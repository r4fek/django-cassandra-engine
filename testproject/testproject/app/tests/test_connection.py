from cassandra import ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from djangotoolbox.db.base import FakeCursor
from mock import patch

from django.db import connections
from django.test import TestCase

from django_cassandra_engine.connection import CassandraConnection


class CassandraConnectionTestCase(TestCase):

    def setUp(self):
        connection = connections['cassandra']
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

    def test_connection_options(self):
        connection = connections['cassandra']
        connection_options = connection.settings_dict['OPTIONS']['connection']
        self.assertEqual(
            self.connection.connection_options, connection_options)

    @patch("cqlengine.connection")
    def test_connection_setup_called_first_time_with_proper_options(
            self, connection_mock):

        settings = connections['cassandra'].settings_dict
        connection_mock.cluster = None
        connection = CassandraConnection(**settings)

        connection_mock.setup.assert_called_once_with(
            connection.hosts, connection.keyspace,
            consistency=settings['OPTIONS']['consistency_level'],
            **settings['OPTIONS']['connection'])

    @patch("django_cassandra_engine.connection.connection")
    def test_connection_setup_called_second_time(
            self, connection_mock):

        settings = connections['cassandra'].settings_dict
        connection_mock.cluster = Cluster()
        CassandraConnection(**settings)

        self.assertFalse(connection_mock.setup.called)

    def test_connection_auth_provider_added_to_connection_options(self):

        settings = connections['cassandra'].settings_dict
        settings['USER'] = 'user'
        settings['PASSWORD'] = 'pass'
        connection = CassandraConnection(**settings)

        self.assertIsInstance(connection.connection_options['auth_provider'],
                              PlainTextAuthProvider)

    def test_connection_auth_provider_not_changed(self):

        settings = connections['cassandra'].settings_dict
        settings['USER'] = 'user'
        settings['PASSWORD'] = 'pass'
        settings['OPTIONS']['connection'] = {}
        settings['OPTIONS']['connection']['auth_provider'] = 'sth'
        connection = CassandraConnection(**settings)

        self.assertEqual(connection.connection_options['auth_provider'],
                         settings['OPTIONS']['connection']['auth_provider'])

    def test_connection_session_options_default_timeout(self):

        session_opts = \
            connections['cassandra'].settings_dict['OPTIONS']['session']
        self.assertEqual(self.connection.session_options, session_opts)
        self.assertEqual(self.connection.session.default_timeout,
                         session_opts.get('default_timeout'))

    def test_connection_consistency_level(self):

        settings = connections['cassandra'].settings_dict
        settings['OPTIONS']['consistency_level'] = ConsistencyLevel.ALL

        connection = CassandraConnection(**settings)

        from cqlengine import connection as cql_connection
        self.assertEqual(connection.consistency, ConsistencyLevel.ALL)
        self.assertEqual(cql_connection.default_consistency_level,
                         ConsistencyLevel.ALL)
