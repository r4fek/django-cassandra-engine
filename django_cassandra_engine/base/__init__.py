try:
    from django.db.backends.base.base import (
        connection_created,
        BaseDatabaseWrapper
    )
except ImportError:
    try:
        from django.db.backends import BaseDatabaseWrapper
        from django.db.backends import connection_created
    except ImportError:
        from django.db.backends.signals import connection_created

from django_cassandra_engine.connection import (
    CassandraConnection,
    FakeConnection
)
from django_cassandra_engine.base.client import CassandraDatabaseClient
from django_cassandra_engine.base.creation import CassandraDatabaseCreation
from django_cassandra_engine.base.schema import CassandraDatabaseSchemaEditor
from django_cassandra_engine.base.features import CassandraDatabaseFeatures
from django_cassandra_engine.base.operations import CassandraDatabaseOperations
from django_cassandra_engine.base.validation import CassandraDatabaseValidation
from django_cassandra_engine.base.introspection import \
    CassandraDatabaseIntrospection
from django_cassandra_engine.utils import CursorWrapper


class Database(object):
    class Error(Exception):
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


class DatabaseWrapper(BaseDatabaseWrapper):

    Database = Database
    vendor = 'cassandra'

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)

        # Set up the associated backend objects
        self.features = CassandraDatabaseFeatures(self)
        self.ops = CassandraDatabaseOperations(self)
        self.client = CassandraDatabaseClient(self)
        self.creation = CassandraDatabaseCreation(self)
        self.validation = CassandraDatabaseValidation(self)
        self.introspection = CassandraDatabaseIntrospection(self)

        self.commit_on_exit = False
        self.connected = False
        self.autocommit = True

        del self.connection

    def get_connection_params(self):
        return {}

    def get_new_connection(self, conn_params):
        return FakeConnection()

    def init_connection_state(self):
        pass

    def _set_autocommit(self, autocommit):
        pass

    def connect(self):
        if not self.connected or self.connection is None:
            settings = self.settings_dict
            self.connection = CassandraConnection(**settings)
            connection_created.send(sender=self.__class__, connection=self)
            self.connected = True

    def __getattr__(self, attr):
        if attr == "connection":
            assert not self.connected
            self.connect()
            return getattr(self, attr)
        raise AttributeError(attr)

    def reconnect(self):

        if self.connected:
            self.connection.close_all()
            del self.connection
            self.connected = False
        self.connect()

    def close(self):
        pass

    def _commit(self):
        pass

    def _rollback(self):
        pass

    def _cursor(self):
        # Error if keyspace for cursor doesn't exist. django-nose uses
        # a cursor to check if it should create a db or not. Any
        # exception will do, and this will raise a KeyError if the
        # keyspace doesn't exist.
        from cassandra.cqlengine import connection
        keyspace = self.settings_dict['NAME']
        connection.cluster.metadata.keyspaces[keyspace]
        return CursorWrapper(self.connection.cursor(), self)

    def schema_editor(self, *args, **kwargs):
        """
        Returns a new instance of this backends' SchemaEditor (Django>=1.7)
        """
        return CassandraDatabaseSchemaEditor(self, *args, **kwargs)
