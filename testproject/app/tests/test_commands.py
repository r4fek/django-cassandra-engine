from itertools import chain
from unittest import TestCase
from mock import patch, call

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

    @patch(COMMANDS_MOD + ".sync_cassandra.create_keyspace_simple")
    @patch(COMMANDS_MOD + ".sync_cassandra.sync_table")
    def test_sync_cassandra_creates_keyspace_and_tables(
            self, sync_table_mock, create_keyspace_mock):

        alias = get_cassandra_db_alias()
        call_command('sync_cassandra', database=alias)
        replication_factor = 1

        all_models = list(chain.from_iterable(
            self.connection.introspection.cql_models.values()))

        create_keyspace_mock.assert_called_once_with(self.keyspace,
                                                     replication_factor)

        for model in all_models:
            sync_table_mock.assert_has_call(call(model))

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
        call_command('flush', database=db_alias, noinput=True,
                     interactive=False)
