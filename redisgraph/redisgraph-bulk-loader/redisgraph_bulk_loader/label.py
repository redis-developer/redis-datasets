import re
import sys
import click
from entity_file import Type, EntityFile
from exceptions import SchemaError


class Label(EntityFile):
    """Handler class for processing Label CSV files."""
    def __init__(self, query_buffer, infile, label_str, config):
        self.id_namespace = None
        self.query_buffer = query_buffer
        super(Label, self).__init__(infile, label_str, config)

    def process_schemaless_header(self, header):
        # The first column is the ID.
        # If this starts with an underscore, it is not a property and should not be introduced to the graph.
        self.id = 0

        for idx, field in enumerate(header):
            self.column_names[idx] = field

        if header[0][0] == '_':
            self.column_names[0] = None

    def post_process_header_with_schema(self, header):
        # No ID field is required if we're only inserting nodes.
        if self.config.store_node_identifiers is False:
            return

        # Verify that exactly one field is labeled ID.
        if self.types.count(Type.ID) != 1:
            raise SchemaError("Node file '%s' should have exactly one ID column."
                              % (self.infile.name))
        self.id = self.types.index(Type.ID) # Track the offset containing the node ID.
        id_field = header[self.id]
        # If the ID field specifies an ID namespace in parentheses like "val:ID(NAMESPACE)", capture the namespace.
        match = re.search(r"\((\w+)\)", id_field)
        if match:
            self.id_namespace = match.group(1)

    def update_node_dictionary(self, identifier):
        """Add identifier->ID pair to dictionary if we are building relations"""
        if identifier in self.query_buffer.nodes:
            sys.stderr.write("Node identifier '%s' was used multiple times - second occurrence at %s:%d\n"
                             % (identifier, self.infile.name, self.reader.line_num))
            if self.config.skip_invalid_nodes is False:
                sys.exit(1)
        self.query_buffer.nodes[identifier] = self.query_buffer.top_node_id
        self.query_buffer.top_node_id += 1

    def process_entities(self):
        entities_created = 0
        with click.progressbar(self.reader, length=self.entities_count, label=self.entity_str) as reader:
            for row in reader:
                self.validate_row(row)

                # Update the node identifier dictionary if necessary
                if self.config.store_node_identifiers:
                    id_field = row[self.id]
                    if self.id_namespace is not None:
                        id_field = self.id_namespace + '.' + str(id_field)
                    self.update_node_dictionary(id_field)

                row_binary = self.pack_props(row)
                row_binary_len = len(row_binary)
                # If the addition of this entity will make the binary token grow too large,
                # send the buffer now.
                # TODO how much of this can be made uniform w/ relations and moved to Querybuffer?
                if self.binary_size + row_binary_len > self.config.max_token_size:
                    self.query_buffer.labels.append(self.to_binary())
                    self.query_buffer.send_buffer()
                    self.reset_partial_binary()
                    # Push the label onto the query buffer again, as there are more entities to process.
                    self.query_buffer.labels.append(self.to_binary())

                self.query_buffer.node_count += 1
                entities_created += 1
                self.binary_size += row_binary_len
                self.binary_entities.append(row_binary)
            self.query_buffer.labels.append(self.to_binary())
        self.infile.close()
        print("%d nodes created with label '%s'" % (entities_created, self.entity_str))
