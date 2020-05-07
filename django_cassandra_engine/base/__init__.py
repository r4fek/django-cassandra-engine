import threading

try:
    from django.db.backends.base.base import (
        connection_created,
        BaseDatabaseWrapper,
    )
except ImportError:
    try:
        from django.db.backends import BaseDatabaseWrapper
        from django.db.backends import connection_created
    except ImportError:
        from django.db.backends.signals import connection_created

from django_cassandra_engine.connection import (
    CassandraConnection,
    FakeConnection,
)
from django_cassandra_engine.base.client import CassandraDatabaseClient
from django_cassandra_engine.base.creation import CassandraDatabaseCreation
from django_cassandra_engine.base.schema import CassandraDatabaseSchemaEditor
from django_cassandra_engine.base.features import CassandraDatabaseFeatures
from django_cassandra_engine.base.operations import CassandraDatabaseOperations
from django_cassandra_engine.base.validation import CassandraDatabaseValidation
from django_cassandra_engine.base.introspection import (
    CassandraDatabaseIntrospection,
)
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

    operators = {
        'exact': '= %s',
        'contains': 'CONTAINS %s',
        'gt': '> %s',
        'gte': '>= %s',
        'lt': '< %s',
        'lte': '<= %s',
    }

    client = None
    # Classes instantiated in __init__().
    client_class = CassandraDatabaseClient
    creation_class = CassandraDatabaseCreation
    features_class = CassandraDatabaseFeatures
    introspection_class = CassandraDatabaseIntrospection
    ops_class = CassandraDatabaseOperations
    validation_class = CassandraDatabaseValidation

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)

        self.commit_on_exit = False
        self.connected = False
        self.autocommit = True
        self._connect_lock = threading.RLock()

        if self.client is None:
            # Set up the associated backend objects
            self.features = CassandraDatabaseFeatures(self)
            self.ops = CassandraDatabaseOperations(self)
            self.client = CassandraDatabaseClient(self)
            self.creation = CassandraDatabaseCreation(self)
            self.validation = CassandraDatabaseValidation(self)
            self.introspection = CassandraDatabaseIntrospection(self)

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
        with self._connect_lock:
            if not self.connected or self.connection is None:
                settings = self.settings_dict
                self.connection = CassandraConnection(self.alias, **settings)
                connection_created.send(sender=self.__class__, connection=self)
                self.connected = True

    def __getattr__(self, attr):
        if attr == "connection":
            assert not self.connected
            self.connect()
            return getattr(self, attr)
        raise AttributeError(attr)

    def reconnect(self):
        with self._connect_lock:
            if self.connected:
                self.connection.unregister()
                del self.connection
                self.connected = False
            self.connect()

    def close_if_unusable_or_obsolete(self):
        self.connect()

    def close(self):
        pass

    def _commit(self):
        pass

    def _rollback(self):
        pass

    def _cursor(self, *args, **kwargs):
        keyspace = self.settings_dict['NAME']
        if (
            not self.connection.cluster.schema_metadata_enabled
            and keyspace not in self.connection.cluster.metadata.keyspaces
        ):
            self.connection.cluster.refresh_schema_metadata()

        self.connection.cluster.metadata.keyspaces[keyspace]
        return CursorWrapper(self.connection.cursor(), self)

    def schema_editor(self, *args, **kwargs):
        """
        Returns a new instance of this backends' SchemaEditor (Django>=1.7)
        """
        return CassandraDatabaseSchemaEditor(self, *args, **kwargs)
