from cassandra.cluster import Cluster
from djangotoolbox.db.base import FakeCursor

from django.db import connection
from django.test import TestCase

from django_cassandra_engine.connection import CassandraConnection


class CassandraConnectionTestCase(TestCase):

    def setUp(self):

        self.connection = CassandraConnection(**connection.settings_dict)

    def test_cursor(self):

        self.assertIsInstance(self.connection.cursor(), FakeCursor)

    def test_connected_to_db(self):

        from cqlengine import connection as cql_connection

        self.assertIsInstance(cql_connection.cluster, Cluster)
        self.assertIsNotNone(cql_connection.session)

    def test_session_property(self):

        from cqlengine import connection as cql_connection

        self.assertEqual(self.connection.session, cql_connection.session)

    def test_cluster_property(self):

        from cqlengine import connection as cql_connection

        self.assertEqual(self.connection.cluster, cql_connection.cluster)
