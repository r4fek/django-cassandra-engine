from django.db.backends import connection_created
from djangotoolbox.db.base import (
    NonrelDatabaseClient,
    NonrelDatabaseFeatures,
    NonrelDatabaseIntrospection,
    NonrelDatabaseOperations,
    NonrelDatabaseValidation,
    NonrelDatabaseWrapper
)
from django_cassandra_engine.connection import CassandraConnection
from django_cassandra_engine.creation import DatabaseCreation


class DatabaseFeatures(NonrelDatabaseFeatures):
    string_based_auto_field = True


class DatabaseOperations(NonrelDatabaseOperations):

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        """
        SQL flush is not available in this engine
        """
        return ''


class DatabaseClient(NonrelDatabaseClient):
    pass


class DatabaseValidation(NonrelDatabaseValidation):
    pass


class DatabaseIntrospection(NonrelDatabaseIntrospection):
    pass


class DatabaseWrapper(NonrelDatabaseWrapper):

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)

        # Set up the associated backend objects
        self.features = DatabaseFeatures(self)
        self.ops = DatabaseOperations(self)
        self.client = DatabaseClient(self)
        self.creation = DatabaseCreation(self)
        self.validation = DatabaseValidation(self)
        self.introspection = DatabaseIntrospection(self)

    def connect(self):

        settings = self.settings_dict

        self.connection = CassandraConnection(**settings)
        connection_created.send(sender=self.__class__, connection=self)

    def _commit(self):
        pass

    def _rollback(self):
        pass
