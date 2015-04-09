try:
    from django.db.backends.base.base import BaseDatabaseWrapper
except ImportError:
    from django.db.backends import BaseDatabaseWrapper

from django_cassandra_engine.connection import FakeConnection, Cursor


class Database(object):
    class Error(StandardError):
        pass

    class InterfaceError(Error):
        pass

    class DatabaseError(Error):
        pass

    class DataError(DatabaseError):
        pass

    class OperationalError(DatabaseError):
        pass

    class IntegrityError(DatabaseError):
        pass

    class InternalError(DatabaseError):
        pass

    class ProgrammingError(DatabaseError):
        pass

    class NotSupportedError(DatabaseError):
        pass


class CassandraDatabaseWrapper(BaseDatabaseWrapper):

    Database = Database

    def get_connection_params(self):
        return {}

    def get_new_connection(self, conn_params):
        return FakeConnection()

    def init_connection_state(self):
        pass

    def _set_autocommit(self, autocommit):
        pass

    def _cursor(self):
        return FakeCursor()
