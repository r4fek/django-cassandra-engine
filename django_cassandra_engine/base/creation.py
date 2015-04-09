from cassandra.cqlengine.management import (
    create_keyspace_simple,
    drop_keyspace
)

import django
if django.VERSION[0:2] >= (1, 8):
    from django.db.backends.base.creation import BaseDatabaseCreation
else:
    from django.db.backends.creation import BaseDatabaseCreation


class CassandraDatabaseCreation(BaseDatabaseCreation):

    def create_test_db(self, verbosity=1, autoclobber=False, **kwargs):
        """
        Creates a test database, prompting the user for confirmation if the
        database already exists. Returns the name of the test database created.
        """

        # Don't import django.core.management if it isn't needed.
        from django.core.management import call_command
        from django.conf import settings

        # If using django-nose, its runner has already set the db name
        # to test_*, so restore it here so that all the models for the
        # live keyspace can be found.
        self.connection.connection.keyspace = \
            self.connection.settings_dict['NAME']
        test_database_name = self._get_test_db_name()

        # Set all models keyspace to the test keyspace
        self.set_models_keyspace(test_database_name)

        if verbosity >= 1:
            test_db_repr = ''
            if verbosity >= 2:
                test_db_repr = " ('%s')" % test_database_name
            print("Creating test database for alias '%s'%s..." % (
                self.connection.alias, test_db_repr))

        self.connection.connect()
        options = self.connection.settings_dict.get('OPTIONS', {})
        replication_opts = options.get('replication', {})
        replication_factor = replication_opts.pop('replication_factor', 1)

        create_keyspace_simple(self.connection.settings_dict['NAME'],
                               replication_factor)

        settings.DATABASES[self.connection.alias]["NAME"] = test_database_name
        self.connection.settings_dict["NAME"] = test_database_name

        self.connection.reconnect()

        # Report syncdb messages at one level lower than that requested.
        # This ensures we don't get flooded with messages during testing
        # (unless you really ask to be flooded)
        call_command(
            'sync_cassandra',
            verbosity=max(verbosity - 1, 0),
            interactive=False,
            database=self.connection.alias,
            load_initial_data=False
        )

        return test_database_name

    def _destroy_test_db(self, test_database_name, verbosity=1, **kwargs):

        drop_keyspace(test_database_name)

    def set_models_keyspace(self, keyspace):
        """Set keyspace for all connection models"""
        for models in self.connection.introspection.cql_models.values():
            for model in models:
                model.__keyspace__ = keyspace
