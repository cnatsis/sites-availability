import json

import pandas as pd
import psycopg2
from psycopg2 import sql

from src.utils import datetime_convert
from src.connectors import AivenConnector
from src.utils import constants


class PostgreSQLConnector:
    """
    A class that interacts with PostgreSQL (Aiven PostgreSQL managed service)

    Usage:
    con = PostgreSQLConnector()

    SELECT query example
    res = con.run_query('select * from my_table')

    INSERT example
    res = con.insert('my_table', {"my_field": <value>})
    """

    def __init__(self):
        """
        Initializes a connection with PostgreSQL database.
        """
        self.aiven = AivenConnector(constants.config)
        self.pg = self.aiven.get_service(constants.AIVEN_PROJECT, constants.AIVEN_PG_NAME)
        self.connection = psycopg2.connect(self.pg["service_uri"])
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

    def run_from_file(self, file):
        """
        Run SQL query from file
        :param file: file path
        """
        with open(file, "r") as sql_file:
            print(f"Executing query from file '{file}'...")
            self.cursor.execute(sql_file.read())
            self.connection.commit()
            sql_file.close()
