from django.db.backends.base.operations import BaseDatabaseOperations
from django_cassandra_engine.utils import get_cassandra_connection


class CassandraDatabaseOperations(BaseDatabaseOperations):
    def pk_default_value(self):
        """
        Returns None, to be interpreted by back-ends as a request to
        generate a new key for an "inserted" object.
        """
        return None

    def quote_name(self, name):
        """
        Does not do any quoting, as it is not needed for most NoSQL
        databases.
        """
        return name

    def prep_for_like_query(self, value):
        """
        Does no conversion, parent string-cast is SQL specific.
        """
        return value

    def prep_for_iexact_query(self, value):
        """
        Does no conversion, parent string-cast is SQL specific.
        """
        return value

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        """
        Truncate all existing tables in current keyspace.

        :returns: an empty list
        """

        if tables:
            cql_list = []

            for table in tables:
                cql_list.append(f"TRUNCATE {table}")
            return cql_list
        return []

    def execute_sql_flush(self, using, cql_list):
        for cql in cql_list:
            self.connection.connection.execute(cql)

    def prepare_sql_script(self, sql):
        return [sql]
