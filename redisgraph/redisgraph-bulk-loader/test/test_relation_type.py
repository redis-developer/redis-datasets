import os
import csv
import unittest
from redisgraph_bulk_loader.config import Config
from redisgraph_bulk_loader.relation_type import RelationType


class TestBulkLoader(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        """Delete temporary files"""
        os.remove('/tmp/relations.tmp')

    def test01_process_schemaless_header(self):
        """Verify that a schema-less header is parsed properly."""
        with open('/tmp/relations.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(['START_ID', 'END_ID', 'property'])
            out.writerow([0, 0, 'prop1'])
            out.writerow([1, 1, 'prop2'])

        config = Config()
        reltype = RelationType(None, '/tmp/relations.tmp', 'RelationTest', config)
        self.assertEqual(reltype.start_id, 0)
        self.assertEqual(reltype.end_id, 1)
        self.assertEqual(reltype.entity_str, 'RelationTest')
        self.assertEqual(reltype.prop_count, 1)
        self.assertEqual(reltype.entities_count, 2)

    def test02_process_header_with_schema(self):
        """Verify that a header with a schema is parsed properly."""
        with open('/tmp/relations.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(['End:END_ID(EndNamespace)', 'Start:START_ID(StartNamespace)', 'property:STRING'])
            out.writerow([0, 0, 'prop1'])
            out.writerow([1, 1, 'prop2'])

        config = Config(enforce_schema=True)
        reltype = RelationType(None, '/tmp/relations.tmp', 'RelationTest', config)
        self.assertEqual(reltype.start_id, 1)
        self.assertEqual(reltype.start_namespace, 'StartNamespace')
        self.assertEqual(reltype.end_id, 0)
        self.assertEqual(reltype.end_namespace, 'EndNamespace')
        self.assertEqual(reltype.entity_str, 'RelationTest')
        self.assertEqual(reltype.prop_count, 1)
        self.assertEqual(reltype.entities_count, 2)
        self.assertEqual(reltype.types[0].name, 'END_ID')
        self.assertEqual(reltype.types[1].name, 'START_ID')
        self.assertEqual(reltype.types[2].name, 'STRING')
