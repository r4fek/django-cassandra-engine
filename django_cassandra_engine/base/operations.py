import django
if django.VERSION[0:2] >= (1, 8):
    from django.db.backends.base.operations import BaseDatabaseOperations
else:
    from django.db.backends import BaseDatabaseOperations


class CassandraDatabaseOperations(BaseDatabaseOperations):

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        """
        Truncate all existing tables in current keyspace.

        :returns: an empty list
        """

        for table in tables:
            qs = "TRUNCATE {}".format(table)
            self.connection.connection.execute(qs)

        return []
