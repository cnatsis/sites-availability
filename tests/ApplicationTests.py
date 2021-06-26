import json
import unittest

from src import SitesAvailability, utils, connectors


class ApplicationTests(unittest.TestCase):

    def test_get_site_metrics_error(self):
        sites_availability = SitesAvailability()
        site = 'https://www.google.coma'
        metrics = sites_availability.get_site_metrics(site)
        self.assertEqual(metrics['type'], 'ERROR')

    def test_get_site_metrics_empty_error(self):
        sites_availability = SitesAvailability()
        site = None
        metrics = sites_availability.get_site_metrics(site)
        self.assertEqual(metrics['type'], 'ERROR')

    def test_get_site_metrics_success(self):
        sites_availability = SitesAvailability()
        site = 'https://www.google.com'
        metrics = sites_availability.get_site_metrics(site)
        self.assertEqual(metrics['type'], 'SUCCESS')

    def test_file_not_exists(self):
        file_name = 'test.txt'
        file_content = utils.read_file_to_list(file_name)
        self.assertEqual(file_content, [])

    def test_prepare_insert_statement(self):
        pg = connectors.PostgreSQLConnector("localhost", 5432, "sites", "postgres", "postgres")
        insert_stmt = pg.prepare_insert_statement('test', {"field_1": "value1", "field_2": "value2"})
        expected_stmt = """INSERT INTO "test" ("field_1", "field_2") values (%(field_1)s, %(field_2)s)"""
        self.assertEqual(insert_stmt.as_string(pg.connection), expected_stmt)

    def test_sql_injection_prepare_statement(self):
        pg = connectors.PostgreSQLConnector("localhost", 5432, "sites", "postgres", "postgres")
        insert_stmt = pg.prepare_insert_statement('test', {"field_1": "null); DELETE FROM a; --"})
        expected_stmt = """INSERT INTO "test" ("field_1") values (%(field_1)s)"""
        self.assertEqual(insert_stmt.as_string(pg.connection), expected_stmt)

    def test_pg_insert_sql_injection(self):
        pg = connectors.PostgreSQLConnector("localhost", 5432, "sites", "postgres", "postgres")
        payload = {"type": "null); DROP TABLE error_requests; --"}
        pg.insert("error_requests", payload)

        # Assert table exists and returns a count query
        pg_res = pg.run_query("SELECT COUNT(*) FROM error_requests")
        self.assertGreaterEqual(json.loads(pg_res)[0]['count'], 0)

    def test_pg_query_df(self):
        pg = connectors.PostgreSQLConnector("localhost", 5432, "sites", "postgres", "postgres")
        pg_res = pg.run_query('SELECT COUNT(*) FROM error_requests', 'df')
        self.assertGreaterEqual(pg_res.iloc[0]['count'], 0)

    def test_pg_insert_exception(self):
        pg = connectors.PostgreSQLConnector("localhost", 5432, "sites", "postgres", "postgres")
        payload = {"id": "null"}
        pg.insert("error_requests", payload)
        self.assertEqual("InFailedSqlTransaction", pg.insert("error_requests", payload))


if __name__ == '__main__':
    unittest.main()
