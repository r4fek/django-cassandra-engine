from cassandra.cluster import Cluster
from djangotoolbox.db.base import FakeCursor
from mock import patch, Mock

from django.db import connection
from django.test import TestCase

from django_cassandra_engine.connection import CassandraConnection


class CassandraConnectionTestCase(TestCase):

    def test_cursor(self):

        conn = CassandraConnection(**connection.settings_dict)
        self.assertIsInstance(conn.cursor(), FakeCursor)

    def test_connected_to_db(self):

        from cqlengine import connection as cql_connection
        CassandraConnection(**connection.settings_dict)

        self.assertIsInstance(cql_connection.cluster, Cluster)

    @patch('django_cassandra_engine.connection.CassandraConnection.cluster')
    def test_close(self, cluster_mock):
        from cqlengine import connection as cql_connection
        shutdown_mock = Mock()
        cluster_mock.shutdown = shutdown_mock

        self.assertIsNotNone(cql_connection.cluster)
        conn = CassandraConnection(**connection.settings_dict)
        conn.close()

        shutdown_mock.assert_called_once()
        self.assertIsNone(cql_connection.cluster)
