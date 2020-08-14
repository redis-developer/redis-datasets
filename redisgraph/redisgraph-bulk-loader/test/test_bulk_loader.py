# -*- coding: utf-8 -*-

import os
import csv
import redis
import unittest
from redisgraph import Graph
from click.testing import CliRunner
from redisgraph_bulk_loader.bulk_insert import bulk_insert

# Globals for validating example graph
person_count = ""
country_count = ""
knows_count = ""
visited_count = ""


def row_count(in_csv):
    """Utility function for counting rows in a CSV file."""
    with open(in_csv) as f:
        # Increment idx for each line
        for idx, l in enumerate(f):
            pass
    # idx is equal to # of lines - 1 due to 0 indexing.
    # This is the count we want, as the header line should  be ignored.
    return idx


class TestBulkLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Instantiate a new Redis connection
        """
        cls.redis_con = redis.Redis(host='localhost', port=6379, decode_responses=True)
        cls.redis_con.flushall()

    @classmethod
    def tearDownClass(cls):
        """Delete temporary files"""
        os.remove('/tmp/nodes.tmp')
        os.remove('/tmp/relations.tmp')
        cls.redis_con.flushall()

    def validate_exception(self, res, expected_msg):
        self.assertNotEqual(res.exit_code, 0)
        self.assertIn(expected_msg, str(res.exception))

    def test01_social_graph(self):
        """Build the graph in 'example' and validate the created graph."""
        global person_count
        global country_count
        global knows_count
        global visited_count

        graphname = "social"
        runner = CliRunner()

        csv_path = os.path.dirname(os.path.abspath(__file__)) + '/../example/'
        person_file = csv_path + 'Person.csv'
        country_file = csv_path + 'Country.csv'
        knows_file = csv_path + 'KNOWS.csv'
        visited_file = csv_path + 'VISITED.csv'

        # Set the globals for node edge counts, as they will be reused.
        person_count = str(row_count(person_file))
        country_count = str(row_count(country_file))
        knows_count = str(row_count(knows_file))
        visited_count = str(row_count(visited_file))

        res = runner.invoke(bulk_insert, ['--nodes', person_file,
                                          '--nodes', country_file,
                                          '--relations', knows_file,
                                          '--relations', visited_file,
                                          graphname])

        # The script should report 27 overall node creations and 48 edge creations.
        self.assertEqual(res.exit_code, 0)
        self.assertIn("27 nodes created", res.output)
        self.assertIn("48 relations created", res.output)

        # Validate creation count by label/type
        self.assertIn(person_count + " nodes created with label 'Person'", res.output)
        self.assertIn(country_count + " nodes created with label 'Country'", res.output)
        self.assertIn(knows_count + " relations created for type 'KNOWS'", res.output)
        self.assertIn(visited_count + " relations created for type 'VISITED'", res.output)

        # Open the constructed graph.
        graph = Graph('social', self.redis_con)
        query_result = graph.query("MATCH (p:Person) RETURN p.name, p.age, p.gender, p.status ORDER BY p.name")
        # Verify that the Person label exists, has the correct attributes, and is properly populated.
        expected_result = [['Ailon Velger', 32, 'male', 'married'],
                           ['Alon Fital', 32, 'male', 'married'],
                           ['Boaz Arad', 31, 'male', 'married'],
                           ['Gal Derriere', 26, 'male', 'single'],
                           ['Jane Chernomorin', 31, 'female', 'married'],
                           ['Lucy Yanfital', 30, 'female', 'married'],
                           ['Mor Yesharim', 31, 'female', 'married'],
                           ['Noam Nativ', 34, 'male', 'single'],
                           ['Omri Traub', 33, 'male', 'single'],
                           ['Ori Laslo', 32, 'male', 'married'],
                           ['Roi Lipman', 32, 'male', 'married'],
                           ['Shelly Laslo Rooz', 31, 'female', 'married'],
                           ['Tal Doron', 32, 'male', 'single'],
                           ['Valerie Abigail Arad', 31, 'female', 'married']]
        self.assertEqual(query_result.result_set, expected_result)

        # Verify that the Country label exists, has the correct attributes, and is properly populated.
        query_result = graph.query('MATCH (c:Country) RETURN c.name ORDER BY c.name')
        expected_result = [['Amsterdam'],
                           ['Andora'],
                           ['Canada'],
                           ['China'],
                           ['Germany'],
                           ['Greece'],
                           ['Italy'],
                           ['Japan'],
                           ['Kazakhstan'],
                           ['Prague'],
                           ['Russia'],
                           ['Thailand'],
                           ['USA']]
        self.assertEqual(query_result.result_set, expected_result)

        # Validate that the expected relations and properties have been constructed
        query_result = graph.query('MATCH (a)-[e:KNOWS]->(b) RETURN a.name, e.relation, b.name ORDER BY e.relation, a.name, b.name')
        expected_result = [['Ailon Velger', 'friend', 'Noam Nativ'],
                           ['Alon Fital', 'friend', 'Gal Derriere'],
                           ['Alon Fital', 'friend', 'Mor Yesharim'],
                           ['Boaz Arad', 'friend', 'Valerie Abigail Arad'],
                           ['Roi Lipman', 'friend', 'Ailon Velger'],
                           ['Roi Lipman', 'friend', 'Alon Fital'],
                           ['Roi Lipman', 'friend', 'Boaz Arad'],
                           ['Roi Lipman', 'friend', 'Omri Traub'],
                           ['Roi Lipman', 'friend', 'Ori Laslo'],
                           ['Roi Lipman', 'friend', 'Tal Doron'],
                           ['Ailon Velger', 'married', 'Jane Chernomorin'],
                           ['Alon Fital', 'married', 'Lucy Yanfital'],
                           ['Ori Laslo', 'married', 'Shelly Laslo Rooz']]
        self.assertEqual(query_result.result_set, expected_result)

        query_result = graph.query('MATCH (a)-[e:VISITED]->(b) RETURN a.name, e.purpose, b.name ORDER BY e.purpose, a.name, b.name')

        expected_result = [['Alon Fital', 'both', 'Prague'],
                           ['Alon Fital', 'both', 'USA'],
                           ['Boaz Arad', 'both', 'Amsterdam'],
                           ['Boaz Arad', 'both', 'USA'],
                           ['Jane Chernomorin', 'both', 'USA'],
                           ['Lucy Yanfital', 'both', 'USA'],
                           ['Roi Lipman', 'both', 'Prague'],
                           ['Tal Doron', 'both', 'USA'],
                           ['Gal Derriere', 'business', 'Amsterdam'],
                           ['Mor Yesharim', 'business', 'Germany'],
                           ['Ori Laslo', 'business', 'China'],
                           ['Ori Laslo', 'business', 'USA'],
                           ['Roi Lipman', 'business', 'USA'],
                           ['Tal Doron', 'business', 'Japan'],
                           ['Alon Fital', 'pleasure', 'Greece'],
                           ['Jane Chernomorin', 'pleasure', 'Amsterdam'],
                           ['Jane Chernomorin', 'pleasure', 'Greece'],
                           ['Lucy Yanfital', 'pleasure', 'Kazakhstan'],
                           ['Lucy Yanfital', 'pleasure', 'Prague'],
                           ['Mor Yesharim', 'pleasure', 'Greece'],
                           ['Mor Yesharim', 'pleasure', 'Italy'],
                           ['Noam Nativ', 'pleasure', 'Amsterdam'],
                           ['Noam Nativ', 'pleasure', 'Germany'],
                           ['Noam Nativ', 'pleasure', 'Thailand'],
                           ['Omri Traub', 'pleasure', 'Andora'],
                           ['Omri Traub', 'pleasure', 'Greece'],
                           ['Omri Traub', 'pleasure', 'USA'],
                           ['Ori Laslo', 'pleasure', 'Canada'],
                           ['Roi Lipman', 'pleasure', 'Japan'],
                           ['Shelly Laslo Rooz', 'pleasure', 'Canada'],
                           ['Shelly Laslo Rooz', 'pleasure', 'China'],
                           ['Shelly Laslo Rooz', 'pleasure', 'USA'],
                           ['Tal Doron', 'pleasure', 'Andora'],
                           ['Valerie Abigail Arad', 'pleasure', 'Amsterdam'],
                           ['Valerie Abigail Arad', 'pleasure', 'Russia']]
        self.assertEqual(query_result.result_set, expected_result)

    def test02_private_identifiers(self):
        """Validate that private identifiers are not added to the graph."""
        graphname = "tmpgraph1"
        # Write temporary files
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(["_identifier", "nodename"])
            out.writerow([0, "a"])
            out.writerow([5, "b"])
            out.writerow([3, "c"])
        with open('/tmp/relations.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(["src", "dest"])
            out.writerow([0, 3])
            out.writerow([5, 3])

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          '--relations', '/tmp/relations.tmp',
                                          graphname], catch_exceptions=False)

        # The script should report 3 node creations and 2 edge creations
        self.assertEqual(res.exit_code, 0)
        self.assertIn('3 nodes created', res.output)
        self.assertIn('2 relations created', res.output)

        tmp_graph = Graph(graphname, self.redis_con)
        # The field "_identifier" should not be a property in the graph
        query_result = tmp_graph.query('MATCH (a) RETURN a')

        for propname in query_result.header:
            self.assertNotIn('_identifier', propname)

    def test03_reused_identifier(self):
        """Expect failure on reused identifiers."""
        graphname = "tmpgraph2"
        # Write temporary files
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(["_identifier", "nodename"])
            out.writerow([0, "a"])
            out.writerow([5, "b"])
            out.writerow([0, "c"]) # reused identifier
        with open('/tmp/relations.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(["src", "dest"])
            out.writerow([0, 3])

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          '--relations', '/tmp/relations.tmp',
                                          graphname], catch_exceptions=False)

        # The script should fail because a node identifier is reused
        self.assertNotEqual(res.exit_code, 0)
        self.assertIn('used multiple times', res.output)

        # Run the script again without creating relations
        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          graphname], catch_exceptions=False)

        # The script should succeed and create 3 nodes
        self.assertEqual(res.exit_code, 0)
        self.assertIn('3 nodes created', res.output)

    def test04_batched_build(self):
        """
        Create a graph using many batches.
        Reuses the inputs of test01_social_graph
        """
        graphname = "batched_graph"
        runner = CliRunner()

        csv_path = os.path.dirname(os.path.abspath(__file__)) + '/../example/'
        person_file = csv_path + 'Person.csv'
        country_file = csv_path + 'Country.csv'
        knows_file = csv_path + 'KNOWS.csv'
        visited_file = csv_path + 'VISITED.csv'
        csv_path = os.path.dirname(os.path.abspath(__file__)) + '/../../demo/bulk_insert/resources/'
        # Build the social graph again with a max token count of 1.
        res = runner.invoke(bulk_insert, ['--nodes', person_file,
                                          '--nodes', country_file,
                                          '--relations', knows_file,
                                          '--relations', visited_file,
                                          '--max-token-count', 1,
                                          graphname], catch_exceptions=False)

        # The script should report 27 overall node creations and 48 edge creations.
        self.assertEqual(res.exit_code, 0)
        self.assertIn("27 nodes created", res.output)
        self.assertIn("48 relations created", res.output)

        # Validate creation count by label/type
        self.assertIn(person_count + " nodes created with label 'Person'", res.output)
        self.assertIn(country_count + " nodes created with label 'Country'", res.output)
        self.assertIn(knows_count + " relations created for type 'KNOWS'", res.output)
        self.assertIn(visited_count + " relations created for type 'VISITED'", res.output)

        original_graph = Graph('social', self.redis_con)
        new_graph = Graph(graphname, self.redis_con)

        # Newly-created graph should be identical to graph created in single bulk command
        original_result = original_graph.query('MATCH (p:Person) RETURN p, ID(p) ORDER BY p.name')
        new_result = new_graph.query('MATCH (p:Person) RETURN p, ID(p) ORDER BY p.name')
        self.assertEqual(original_result.result_set, new_result.result_set)

        original_result = original_graph.query('MATCH (a)-[e:KNOWS]->(b) RETURN a.name, e, b.name ORDER BY e.relation, a.name')
        new_result = new_graph.query('MATCH (a)-[e:KNOWS]->(b) RETURN a.name, e, b.name ORDER BY e.relation, a.name')
        self.assertEqual(original_result.result_set, new_result.result_set)

    def test05_script_failures(self):
        """Validate that the bulk loader fails gracefully on invalid inputs and arguments"""

        graphname = "tmpgraph3"
        # Write temporary files
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(["id", "nodename"])
            out.writerow([0]) # Wrong number of properites

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          graphname])

        # The script should fail because a row has the wrong number of fields
        self.validate_exception(res, "Expected 2 columns")

        # Write temporary files
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(["id", "nodename"])
            out.writerow([0, "a"])

        with open('/tmp/relations.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(["src"]) # Incomplete relation description
            out.writerow([0])

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          '--relations', '/tmp/relations.tmp',
                                          graphname])

        # The script should fail because a row has the wrong number of fields
        self.validate_exception(res, "should have at least 2 elements")

        with open('/tmp/relations.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(["src", "dest"])
            out.writerow([0, "fakeidentifier"])

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          '--relations', '/tmp/relations.tmp',
                                          graphname])

        # The script should fail because an invalid node identifier was used
        self.validate_exception(res, "fakeidentifier")

    def test06_property_types(self):
        """Verify that numeric, boolean, and string types are properly handled"""

        graphname = "tmpgraph4"
        # Write temporary files
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(['numeric', 'mixed', 'bool'])
            out.writerow([0.2, 'string_prop_1', True])
            out.writerow([5, "notnull", False])
            out.writerow([7, 100, False])
        with open('/tmp/relations.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(["src", "dest", "prop"])
            out.writerow([0.2, 5, True])
            out.writerow([5, 7, 3.5])
            out.writerow([7, 0.2, 'edge_prop'])

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          '--relations', '/tmp/relations.tmp',
                                          graphname], catch_exceptions=False)

        self.assertEqual(res.exit_code, 0)
        self.assertIn('3 nodes created', res.output)
        self.assertIn('3 relations created', res.output)

        graph = Graph(graphname, self.redis_con)
        query_result = graph.query('MATCH (a)-[e]->() RETURN a.numeric, a.mixed, a.bool, e.prop ORDER BY a.numeric, e.prop')
        expected_result = [[0.2, 'string_prop_1', True, True],
                           [5, 'notnull', False, 3.5],
                           [7, 100, False, 'edge_prop']]

        # The graph should have the correct types for all properties
        self.assertEqual(query_result.result_set, expected_result)

    def test07_utf8(self):
        """Verify that numeric, boolean, and null types are properly handled"""
        graphname = "tmpgraph5"
        # Write temporary files
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(['id', 'utf8_str_ß'])
            out.writerow([0, 'Straße'])
            out.writerow([1, 'auslösen'])
            out.writerow([2, 'zerstören'])
            out.writerow([3, 'français'])
            out.writerow([4, 'américaine'])
            out.writerow([5, 'épais'])
            out.writerow([6, '中國的'])
            out.writerow([7, '英語'])
            out.writerow([8, '美國人'])

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          graphname], catch_exceptions=False)

        assert res.exit_code == 0
        assert '9 nodes created' in res.output

        graph = Graph(graphname, self.redis_con)
        # The non-ASCII property string must be escaped backticks to parse correctly
        query_result = graph.query("""MATCH (a) RETURN a.`utf8_str_ß` ORDER BY a.id""")
        expected_strs = [['Straße'],
                         ['auslösen'],
                         ['zerstören'],
                         ['français'],
                         ['américaine'],
                         ['épais'],
                         ['中國的'],
                         ['英語'],
                         ['美國人']]

        for i, j in zip(query_result.result_set, expected_strs):
            self.assertEqual(repr(i), repr(j))

    def test08_nonstandard_separators(self):
        """Validate use of non-comma delimiters in input files."""

        graphname = "tmpgraph6"
        inputs = [['prop_a', 'prop_b', 'prop_c'],
                  ['val1', 5, True],
                  [10.5, 'a', False]]
        # Write temporary files
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            # Open writer with pipe separator.
            out = csv.writer(csv_file, delimiter='|',)
            for row in inputs:
                out.writerow(row)

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          '--separator', '|',
                                          graphname], catch_exceptions=False)

        self.assertEqual(res.exit_code, 0)
        self.assertIn('2 nodes created', res.output)

        graph = Graph(graphname, self.redis_con)
        query_result = graph.query('MATCH (a) RETURN a.prop_a, a.prop_b, a.prop_c ORDER BY a.prop_a, a.prop_b, a.prop_c')
        expected_result = [['val1', 5, True],
                           [10.5, 'a', False]]

        # The graph should have the correct types for all properties
        self.assertEqual(query_result.result_set, expected_result)

    def test09_schema(self):
        """Validate that the enforce-schema argument is respected"""

        graphname = "tmpgraph7"
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(['str_col:STRING', 'num_col:INT'])
            out.writerow([0, 0])
            out.writerow([1, 1])

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          '--enforce-schema',
                                          graphname], catch_exceptions=False)

        self.assertEqual(res.exit_code, 0)
        self.assertIn('2 nodes created', res.output)

        graph = Graph(graphname, self.redis_con)
        query_result = graph.query('MATCH (a) RETURN a.str_col, a.num_col ORDER BY a.num_col')
        expected_result = [['0', 0],
                           ['1', 1]]

        # The graph should have the correct types for all properties
        self.assertEqual(query_result.result_set, expected_result)

    def test10_invalid_schema(self):
        """Validate that errors are emitted properly with an invalid CSV schema."""

        graphname = "expect_fail"
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(['num_col:INT'])
            out.writerow([5])
            out.writerow([10])
            out.writerow(['str'])
            out.writerow([15])

        runner = CliRunner()
        # Try to parse all cells as integers
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          '--enforce-schema',
                                          graphname])

        # Expect an error.
        self.validate_exception(res, "Could not parse")

    def test11_schema_ignore_columns(self):
        """Validate that columns with the type IGNORE are not inserted."""

        graphname = "ignore_graph"
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(['str_col:STRING', 'ignore_col:IGNORE'])
            out.writerow(['str1', 0])
            out.writerow(['str2', 1])

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          '--enforce-schema',
                                          graphname], catch_exceptions=False)

        self.assertEqual(res.exit_code, 0)
        self.assertIn('2 nodes created', res.output)

        graph = Graph(graphname, self.redis_con)
        query_result = graph.query('MATCH (a) RETURN a ORDER BY a.str_col')

        # The nodes should only have the 'str_col' property
        node_1 = {'str_col': 'str1'}
        node_2 = {'str_col': 'str2'}
        self.assertEqual(query_result.result_set[0][0].properties, node_1)
        self.assertEqual(query_result.result_set[1][0].properties, node_2)

    def test12_no_null_values(self):
        """Validate that NULL inputs are not inserted."""

        graphname = "null_graph"
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(['str_col', 'mixed_col'])
            out.writerow(['str1', True])
            out.writerow(['str2', None])

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes', '/tmp/nodes.tmp',
                                          graphname], catch_exceptions=False)

        self.assertEqual(res.exit_code, 0)
        self.assertIn('2 nodes created', res.output)

        graph = Graph(graphname, self.redis_con)
        query_result = graph.query('MATCH (a) RETURN a ORDER BY a.str_col')

        # Only the first node should only have the 'mixed_col' property
        node_1 = {'str_col': 'str1', 'mixed_col': True}
        node_2 = {'str_col': 'str2'}
        self.assertEqual(query_result.result_set[0][0].properties, node_1)
        self.assertEqual(query_result.result_set[1][0].properties, node_2)

    def test13_id_namespaces(self):
        """Validate that ID namespaces allow for scoped identifiers."""

        graphname = "namespace_graph"
        with open('/tmp/nodes.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(['id:ID(User)', 'name:STRING'])
            out.writerow([0, 'Jeffrey'])
            out.writerow([1, 'Filipe'])

        with open('/tmp/nodes2.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(['id:ID(Post)', 'views:INT'])
            out.writerow([0, 20])
            out.writerow([1, 40])

        with open('/tmp/relations.tmp', mode='w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow([':START_ID(User)', ':END_ID(Post)'])
            out.writerow([0, 0])
            out.writerow([1, 1])

        runner = CliRunner()
        res = runner.invoke(bulk_insert, ['--nodes-with-label', 'User', '/tmp/nodes.tmp',
                                          '--nodes-with-label', 'Post', '/tmp/nodes2.tmp',
                                          '--relations-with-type', 'AUTHOR', '/tmp/relations.tmp',
                                          '--enforce-schema',
                                          graphname], catch_exceptions=False)

        self.assertEqual(res.exit_code, 0)
        self.assertIn('4 nodes created', res.output)
        self.assertIn("2 relations created", res.output)

        graph = Graph(graphname, self.redis_con)
        query_result = graph.query('MATCH (src)-[]->(dest) RETURN src.id, src.name, LABELS(src), dest.id, dest.views, LABELS(dest) ORDER BY src.id')

        expected_result = [[0, 'Jeffrey', 'User', 0, 20, 'Post'],
                           [1, 'Filipe', 'User', 1, 40, 'Post']]
        self.assertEqual(query_result.result_set, expected_result)


if __name__ == '__main__':
    unittest.main()
