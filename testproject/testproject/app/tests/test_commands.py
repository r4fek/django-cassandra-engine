from itertools import chain
from unittest import TestCase
from mock import patch, call

from django.core.management import call_command
from django.db import connections

connection = connections['cassandra']


class SyncdbCommandTestCase(TestCase):

    def setUp(self):
        self.keyspace = connection.settings_dict['NAME']

    @patch(
        "django_cassandra_engine.management.commands.syncdb.create_keyspace")
    @patch("django_cassandra_engine.management.commands.syncdb.sync_table")
    def test_syncdb_creates_keyspace_and_tables(self, sync_table_mock,
                                                create_keyspace_mock):

        call_command('syncdb', database='cassandra')
        options = connection.settings_dict.get('OPTIONS', {})
        replication_opts = options.get('replication', {})
        all_models = list(chain.from_iterable(
            connection.introspection.cql_models.values()))

        create_keyspace_mock.assert_called_once_with(self.keyspace,
                                                     **replication_opts)
        for model in all_models:
            sync_table_mock.assert_has_call(call(model))

    def test_syncdb_of_another_database(self):
        """
        Test if syncdb of another database works as before
        """

        base_command = \
            "django.core.management.commands.syncdb.Command.handle_noargs"
        with patch(base_command) as handle_mock:
            call_command('syncdb', database='mysql')

        handle_mock.assert_called_once()
