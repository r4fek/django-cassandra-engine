from django.db.backends.base.operations import BaseDatabaseOperations


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
        """Does no conversion, parent string-cast is SQL specific."""
        return value

    def prep_for_iexact_query(self, value):
        """Does no conversion, parent string-cast is SQL specific."""
        return value

    def sql_flush(self, style, tables, *args, **kwargs):
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

    def execute_sql_flush(self, *args):
        # In previous django versions first parameter was `using` and second `sql_list`.
        # In Django 3.1 only one parameter `sql_list` is present.
        # One thing is certain though: last parameter is `sql_list`
        for cql in args[-1]:
            self.connection.connection.execute(cql)

    def prepare_sql_script(self, sql):
        return [sql]
