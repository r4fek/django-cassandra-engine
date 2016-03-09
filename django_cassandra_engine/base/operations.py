import django
if django.VERSION[0:2] >= (1, 8):
    from django.db.backends.base.operations import BaseDatabaseOperations
else:
    from django.db.backends import BaseDatabaseOperations


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

        for table in tables:
            qs = "TRUNCATE {}".format(table)
            self.connection.connection.execute(qs)

        return []
