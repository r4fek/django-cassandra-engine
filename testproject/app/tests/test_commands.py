from itertools import chain
from unittest import TestCase, skipIf
from mock import patch, call

import django
from django.core.management import call_command
from django_cassandra_engine.utils import (
    get_cassandra_connection,
    get_cassandra_db_alias
)

COMMANDS_MOD = 'django_cassandra_engine.management.commands'


class SyncCassandraCommandTestCase(TestCase):

    def setUp(self):
        self.connection = get_cassandra_connection()
        self.keyspace = self.connection.settings_dict['NAME']

    @patch(COMMANDS_MOD + '.sync_cassandra.management')
    def test_sync_cassandra_creates_keyspace_and_tables(self, mock_management):

        alias = get_cassandra_db_alias()
        call_command('sync_cassandra', database=alias)
        replication_factor = 1

        all_models = list(chain.from_iterable(
            self.connection.introspection.cql_models.values()))

        mock_management.create_keyspace_simple.assert_called_once_with(
            self.keyspace,
            replication_factor,
            connections=[alias]
        )

        for model in all_models:
            mock_management.sync_table.assert_has_call(call(model))

    @skipIf(django.VERSION >= (1, 9), "Django >=1.9 does not support syncdb")
    def test_syncdb_of_another_database(self):
        """
        Test if syncdb of another database works as before
        """
        import django
        if django.VERSION[0:2] >= (1, 8):
            base_command = \
                "django.core.management.commands.syncdb.Command.handle"
        else:
            base_command = \
                "django.core.management.commands.syncdb.Command.handle_noargs"

        with patch(base_command) as handle_mock:
            call_command('syncdb', database='mysql')

        handle_mock.assert_called_once()


class FlushCommandTestCase(TestCase):

    def test_flush(self):

        db_alias = get_cassandra_db_alias()
        call_command('flush', database=db_alias, interactive=False)


class RunserverCommandTestCase(TestCase):

    @patch('django.core.management.commands.runserver.Command.run')
    def test_runserver_works(self, _):
        call_command('runserver')
