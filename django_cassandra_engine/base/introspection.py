from itertools import chain

from django.db.backends.base.introspection import BaseDatabaseIntrospection
from django_cassandra_engine.utils import get_installed_apps, get_cql_models


class CassandraDatabaseIntrospection(BaseDatabaseIntrospection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cql_models = {}
        self._models_discovered = False

    def _discover_models(self):
        """
        Return a dict containing a list of cassandra.cqlengine.Model classes
        within installed App.
        """

        apps = get_installed_apps()
        connection = self.connection.connection.alias
        keyspace = self.connection.connection.keyspace

        for app in apps:
            self._cql_models[app.__name__] = get_cql_models(
                app, connection=connection, keyspace=keyspace
            )

    @property
    def cql_models(self):
        if not self._models_discovered:
            self._discover_models()
            self._models_discovered = True
        return self._cql_models

    def get_migratable_models(self):
        return self.cql_models

    def installed_models(self, tables):
        return self.cql_models

    def django_table_names(self, only_existing=False, **kwargs):
        """
        Returns a list of all table names that have associated cqlengine models
        and are present in settings.INSTALLED_APPS.
        """

        all_models = list(chain.from_iterable(self.cql_models.values()))
        tables = [
            model.column_family_name(include_keyspace=False)
            for model in all_models
        ]

        return tables

    def table_names(self, cursor=None, **kwargs):
        """
        Returns all table names in current keyspace
        """
        # Avoid migration code being executed
        if cursor:
            return []

        connection = self.connection.connection
        keyspace_name = connection.keyspace
        if (
            not connection.cluster.schema_metadata_enabled
            and keyspace_name not in connection.cluster.metadata.keyspaces
        ):
            connection.cluster.refresh_schema_metadata()

        keyspace = connection.cluster.metadata.keyspaces[keyspace_name]
        return keyspace.tables

    def get_table_list(self, cursor):
        return self.table_names(cursor)

    def sequence_list(self):
        """
        Sequences are not supported
        """
        return []

    def get_sequences(self, *args, **kwargs):
        return []

    def get_relations(self, *_):
        """No relations in nonrel database"""
        return []

    def get_table_description(self, *_):
        """
        Unfortunately we can't use `DESCRIBE table_name` here
        because DESCRIBE isn't part of CQL language..
        """
        return ""

    def get_constraints(self, cursor, table_name):
        return {}

    def get_indexes(self, cursor, table_name):
        return {}
