from cassandra import ConsistencyLevel
from djangotoolbox.db.base import FakeCursor
from mock import patch, Mock

from django.conf import settings
from django.db import connection
from django.test import TestCase

from django_cassandra_engine.connection import CassandraConnection


class CassandraConnectionTestCase(TestCase):

    @patch('django_cassandra_engine.connection.connection.setup')
    def test_setup(self, mock_connection_setup):

        db_settings = settings.DATABASES['default']
        conn = CassandraConnection(**connection.settings_dict)

        self.assertEqual(conn.hosts, db_settings['HOST'].split(','))
        self.assertEqual(conn.keyspace, db_settings['NAME'])
        self.assertEqual(conn.options, db_settings['OPTIONS'])

        mock_connection_setup.assert_called_once_with(
            conn.hosts,
            conn.keyspace,
            consistency=conn.options.get('consistency_level',
                                         ConsistencyLevel.ONE)
        )

    def test_cursor(self):

        conn = CassandraConnection(**connection.settings_dict)
        self.assertIsInstance(conn.cursor(), FakeCursor)

    @patch('django_cassandra_engine.connection.CassandraConnection.cluster')
    def test_close(self, cluster_mock):

        shutdown_mock = Mock()
        cluster_mock.shutdown = shutdown_mock

        conn = CassandraConnection(**connection.settings_dict)
        conn.close()

        shutdown_mock.assert_called_once()
