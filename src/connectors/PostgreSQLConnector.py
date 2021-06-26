import json

import pandas as pd
import psycopg2
from psycopg2 import sql

from src.utils import datetime_convert


class PostgreSQLConnector:
    """
    Usage:
    con = PostgreSQLConnector("localhost", 5432, "schema", "user", "pass")

    SELECT query example
    res = con.run_query('select * from my_table')

    INSERT example
    res = con.insert('my_table', {"my_field": <value>})
    """

    def __init__(self, host, port, database, user, password):
        """
        Initializes a connection with PostgreSQL database.
        :param host: PostgreSQL database IP
        :param port: PostgreSQL database port
        :param database: PostgreSQL database name
        :param user: PostgreSQL database username
        :param password: PostgreSQL database password
        """
        # self.user = user
        # self.password = password
        self.pg = None
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password)
        if self.connection is not None:
            self.cursor = self.connection.cursor()
        else:
            self.cursor = None

    def _get_connection(self):
        """
        Gets active PostgreSQL connection.
        :return: PostgreSQL connection reference
        """
        return self.connection

    def close(self):
        """
        Terminates active PostgreSQL connection
        :return: None
        """
        self.cursor.close()
        self.connection.close()

    @staticmethod
    def prepare_insert_statement(table, fields):
        """
        Prepares insert statement
        :param table: target table
        :param fields: field names
        :return: Expected output INSERT INTO "table_name" ("field_1", "field_1") values (%(field_1)s, %(field_2)s)
        """
        return sql.SQL("INSERT INTO {table} ({fields}) values ({values})") \
            .format(table=sql.Identifier(table),
                    fields=sql.SQL(', ').join(map(sql.Identifier, list(fields))),
                    values=sql.SQL(', ').join(map(sql.Placeholder, list(fields))))

    def insert(self, table, input_object):
        """
        Executes an INSERT query for a given dict
        :param table: table name
        :param input_object: Sample object {"key1": "value1", "key2": "value2"}
        :return: None
        """
        s = self.prepare_insert_statement(table, input_object.keys())
        try:
            self.cursor.execute(s, input_object)
        except Exception as e:
            print("{} exception occurred: {}".format(type(e).__name__, e))
            return type(e).__name__
        self.connection.commit()

    def create_table(self):
        try:
            conn = psycopg2.connect(self.pg["service_uri"])
        except psycopg2.OperationalError as e:
            print("{self.config['pg_name]} service not yet available. Waiting.", json.loads(e)["message"])
            return 1

        with conn:
            with conn.cursor() as cursor:
                with open("sensor_temperature.sql", "r") as table_sql:
                    cursor.execute(table_sql.read())
        return 0

    def run_query(self, query, output_format='json'):
        """
        Executes a given query. Output format can be either JSON, or Pandas DataFrame.
        :param query: Query string
        :param output_format: 'json' for JSON output (default), 'df' for Pandas Data Frame output
        :return: JSON or DataFrame
        """
        self.cursor.execute(query)
        if self.cursor.rowcount != -1:
            res = [dict(line) for line in
                   [zip([column[0] for column in self.cursor.description], row) for row in self.cursor.fetchall()]]
            self.close()
            if output_format == 'df':
                return pd.read_json(json.dumps(res, default=datetime_convert))
            else:
                return json.dumps(res)
