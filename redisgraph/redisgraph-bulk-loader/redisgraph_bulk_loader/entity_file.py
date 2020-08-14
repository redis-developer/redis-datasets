import os
import io
import csv
import math
import struct
from enum import Enum
from exceptions import CSVError, SchemaError


class Type(Enum):
    UNKNOWN = 0
    BOOL = 1
    DOUBLE = 2
    FLOAT = 2       # alias to DOUBLE
    STRING = 3
    LONG = 4
    INT = 4         # alias to LONG
    INTEGER = 4     # alias to LONG
    ID = 5
    START_ID = 6
    END_ID = 7
    IGNORE = 8


def convert_schema_type(in_type):
    try:
        return Type[in_type]
    except KeyError:
        # Handling for ID namespaces
        # TODO think of better alternatives
        if in_type.startswith('ID('):
            return Type.ID
        elif in_type.startswith('START_ID('):
            return Type.START_ID
        elif in_type.startswith('END_ID('):
            return Type.END_ID
        else:
            raise SchemaError("Encountered invalid field type '%s'" % in_type)


# Convert a property field with an enforced type into a binary stream.
# Supported property types are string, integer, float, and boolean.
def typed_prop_to_binary(prop_val, prop_type):
    # All format strings start with an unsigned char to represent our prop_type enum
    format_str = "=B"
    # TODO allow ID type specification
    if prop_type == Type.ID or prop_type == Type.LONG:
        try:
            numeric_prop = int(prop_val)
            return struct.pack(format_str + "q", Type.LONG.value, numeric_prop)
        except (ValueError, struct.error):
            # TODO ugly, rethink
            if prop_type == Type.LONG:
                raise SchemaError("Could not parse '%s' as a long" % prop_val)

    elif prop_type == Type.ID or prop_type == Type.DOUBLE:
        try:
            numeric_prop = float(prop_val)
            if not math.isnan(numeric_prop) and not math.isinf(numeric_prop): # Don't accept non-finite values.
                return struct.pack(format_str + "d", Type.DOUBLE.value, numeric_prop)
        except (ValueError, struct.error):
            # TODO ugly, rethink
            if prop_type == Type.DOUBLE:
                raise SchemaError("Could not parse '%s' as a double" % prop_val)

    elif prop_type == Type.BOOL:
        # If field is 'false' or 'true', it is a boolean
        if prop_val.lower() == 'false':
            return struct.pack(format_str + '?', Type.BOOL.value, False)
        elif prop_val.lower() == 'true':
            return struct.pack(format_str + '?', Type.BOOL.value, True)
        else:
            raise SchemaError("Could not parse '%s' as a boolean" % prop_val)

    elif prop_type == Type.STRING:
        # If we've reached this point, the property is a string
        encoded_str = str.encode(prop_val) # struct.pack requires bytes objects as arguments
        # Encoding len+1 adds a null terminator to the string
        format_str += "%ds" % (len(encoded_str) + 1)
        return struct.pack(format_str, Type.STRING.value, encoded_str)

    # If it hasn't returned by this point, it is trying to set it to a type that it can't adopt
    raise Exception("unable to parse [" + prop_val + "] with type ["+repr(prop_type)+"]")


# Convert a single CSV property field with an inferred type into a binary stream.
# Supported property types are string, integer, float, boolean, and (erroneously) null.
def inferred_prop_to_binary(prop_val):
    # All format strings start with an unsigned char to represent our prop_type enum
    format_str = "=B"
    if prop_val == "":
        # An empty string indicates a NULL property.
        # TODO This is not allowed in Cypher, consider how to handle it here rather than in-module.
        return struct.pack(format_str, 0)

    # Try to parse value as an integer.
    try:
        numeric_prop = int(prop_val)
        return struct.pack(format_str + "q", Type.LONG.value, numeric_prop)
    except (ValueError, struct.error):
        pass

    # Try to parse value as a float.
    try:
        numeric_prop = float(prop_val)
        if not math.isnan(numeric_prop) and not math.isinf(numeric_prop): # Don't accept non-finite values.
            return struct.pack(format_str + "d", Type.DOUBLE.value, numeric_prop)
    except (ValueError, struct.error):
        pass

    # If field is 'false' or 'true', it is a boolean.
    if prop_val.lower() == 'false':
        return struct.pack(format_str + '?', Type.BOOL.value, False)
    elif prop_val.lower() == 'true':
        return struct.pack(format_str + '?', Type.BOOL.value, True)

    # If we've reached this point, the property is a string.
    encoded_str = str.encode(prop_val) # struct.pack requires bytes objects as arguments
    # Encoding len+1 adds a null terminator to the string
    format_str += "%ds" % (len(encoded_str) + 1)
    return struct.pack(format_str, Type.STRING.value, encoded_str)


class EntityFile(object):
    """Superclass for Label and RelationType classes"""
    def __init__(self, filename, label, config):
        # The configurations for this run.
        self.config = config

        # The label or relation type string is the basename of the file
        if label:
            self.entity_str = label
        else:
            self.entity_str = os.path.splitext(os.path.basename(filename))[0]
        # Input file handling
        self.infile = io.open(filename, 'rt')

        # Initialize CSV reader that ignores leading whitespace in each field
        # and does not modify input quote characters
        self.reader = csv.reader(self.infile, delimiter=config.separator, skipinitialspace=True, quoting=config.quoting, escapechar='\\')

        self.packed_header = b''
        self.binary_entities = []
        self.binary_size = 0 # size of binary token

        self.convert_header() # Extract data from header row.
        self.count_entities() # Count number of entities/row in file.
        next(self.reader) # Skip the header row.

    # Count number of rows in file.
    def count_entities(self):
        self.entities_count = 0
        self.entities_count = sum(1 for line in self.infile)
        # seek back
        self.infile.seek(0)
        return self.entities_count

    # Simple input validations for each row of a CSV file
    def validate_row(self, row):
        # Each row should have the same number of fields
        if len(row) != self.column_count:
            raise CSVError("%s:%d Expected %d columns, encountered %d ('%s')"
                           % (self.infile.name, self.reader.line_num, self.column_count, len(row), self.config.separator.join(row)))

    # If part of a CSV file was sent to Redis, delete the processed entities and update the binary size
    def reset_partial_binary(self):
        self.binary_entities = []
        self.binary_size = len(self.packed_header)

    # Convert property keys from a CSV file header into a binary string
    def pack_header(self):
        # String format
        entity_bytes = self.entity_str.encode()
        fmt = "=%dsI" % (len(entity_bytes) + 1) # Unaligned native, entity name, count of properties
        args = [entity_bytes, self.prop_count]
        for idx in range(self.column_count):
            if not self.column_names[idx]:
                continue
            prop = self.column_names[idx].encode()
            fmt += "%ds" % (len(prop) + 1) # encode string with a null terminator
            args.append(prop)
        return struct.pack(fmt, *args)

    def convert_header_with_schema(self, header):
        self.types = [None] * self.column_count # Value type of every column.
        for idx, field in enumerate(header):
            pair = field.split(':')

            # Multiple colons found in column name, emit error.
            # TODO might need to check for backtick escapes
            if len(pair) > 2:
                raise CSVError("Field '%s' had %d colons" % field, len(field))

            # Convert the column type.
            col_type = convert_schema_type(pair[1].upper())

            # If the column did not have a name but the type requires one, emit an error.
            if len(pair[0]) == 0 and col_type not in (Type.ID, Type.START_ID, Type.END_ID, Type.IGNORE):
                raise SchemaError("Each property in the header should be a colon-separated pair")
            else:
                # We have a column name and a type.
                # Only store the name if the column's values should be added as properties.
                if len(pair[0]) > 0 and col_type not in (Type.START_ID, Type.END_ID, Type.IGNORE):
                    self.column_names[idx] = pair[0]

            # Store the column type.
            self.types[idx] = col_type

    def convert_header(self):
        header = next(self.reader)
        self.column_count = len(header)
        self.column_names = [None] * self.column_count   # Property names of every column; None if column does not update graph.

        if self.config.enforce_schema:
            # Use generic logic to convert the header with schema.
            self.convert_header_with_schema(header)
            # The subclass will perform post-processing.
            self.post_process_header_with_schema(header)
        else:
            # The subclass will process the header itself
            self.process_schemaless_header(header)

        # The number of properties is equal to the number of non-skipped columns.
        self.prop_count = self.column_count - self.column_names.count(None)
        self.packed_header = self.pack_header()
        self.binary_size += len(self.packed_header)

    # Convert a list of properties into a binary string
    def pack_props(self, line):
        props = []
        for idx, field in enumerate(line):
            if not self.column_names[idx]:
                continue
            if self.config.enforce_schema:
                props.append(typed_prop_to_binary(field, self.types[idx]))
            else:
                props.append(inferred_prop_to_binary(field))
        return b''.join(p for p in props)

    def to_binary(self):
        return self.packed_header + b''.join(self.binary_entities)
