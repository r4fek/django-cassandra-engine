from copy import copy
from unittest import TestCase

from cassandra import ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.cqlengine import CQLEngineException
from mock import Mock, patch
import mock

from django_cassandra_engine.connection import CassandraConnection, Cursor
from django_cassandra_engine.utils import get_cassandra_connection


class CassandraConnectionTestCase(TestCase):
    def setUp(self):
        self.cassandra_connection = get_cassandra_connection()
        self.connection = self.cassandra_connection.connection
        self.cassandra_connection.connect()

    def test_cursor(self):

        self.assertIsInstance(self.connection.cursor(), Cursor)
        self.assertEqual(self.connection.cursor().connection, self.connection)

    def test_connected_to_db(self):

        from cassandra.cqlengine import connection as cql_connection

        self.assertIsInstance(cql_connection.cluster, Cluster)
        self.assertIsNotNone(cql_connection.session)

    def test_session_property(self):

        from cassandra.cqlengine import connection as cql_connection

        self.assertEqual(
            self.connection.session,
            cql_connection._connections[self.connection.alias].session,
        )

    def test_cluster_property(self):

        from cassandra.cqlengine import connection as cql_connection

        self.assertEqual(
            self.connection.cluster,
            cql_connection._connections[self.connection.alias].cluster,
        )

    def test_connection_options(self):
        connection_options = self.cassandra_connection.settings_dict["OPTIONS"][
            "connection"
        ]

        opts = {
            "lazy_connect": connection_options.pop("lazy_connect", False),
            "retry_connect": connection_options.pop("retry_connect", False),
            "consistency": connection_options.pop("consistency", None),
        }
        self.assertEqual(self.connection.connection_options, opts)

    @patch("django_cassandra_engine.connection.connection")
    def test_register_connection_called_first_time_with_proper_options(
        self, connection_mock
    ):

        settings = self.cassandra_connection.settings_dict
        connection = CassandraConnection("default", **settings)
        connection_mock.get_connection.side_effect = CQLEngineException()
        connection.register()
        connection_mock.register_connection.assert_called_once_with(
            "default",
            hosts=connection.hosts,
            default=mock.ANY,
            cluster_options=connection.cluster_options,
            **connection.connection_options
        )

    @patch("django_cassandra_engine.connection.connection")
    def test_connection_register_called_second_time(self, connection_mock):
        settings = self.cassandra_connection.settings_dict
        CassandraConnection("default", **settings)
        connection_mock.get_connection.side_effect = CQLEngineException()

        self.assertFalse(connection_mock.register_connection.called)

    def test_connection_auth_provider_added_to_connection_options(self):

        settings = self.cassandra_connection.settings_dict
        settings["USER"] = "user"
        settings["PASSWORD"] = "pass"
        connection = CassandraConnection("default", **settings)

        self.assertIsInstance(
            connection.cluster_options["auth_provider"], PlainTextAuthProvider
        )

    @patch("django_cassandra_engine.connection.CassandraConnection.register")
    def test_connection_auth_provider_not_changed(self, register_mock):

        settings = copy(self.cassandra_connection.settings_dict)
        settings["USER"] = "user"
        settings["PASSWORD"] = "pass"
        settings["OPTIONS"]["connection"] = {}
        settings["OPTIONS"]["connection"]["auth_provider"] = "sth"
        connection = CassandraConnection("default", **settings)

        self.assertEqual(
            connection.cluster_options["auth_provider"],
            settings["OPTIONS"]["connection"]["auth_provider"],
        )
        register_mock.assert_called_once()

    def test_connection_session_options_default_timeout(self):

        session_opts = self.cassandra_connection.settings_dict["OPTIONS"]["session"]
        self.assertEqual(self.connection.session_options, session_opts)
        self.assertEqual(
            self.connection.session.default_timeout,
            session_opts.get("default_timeout"),
        )

    def test_connection_session_default_consistency(self):

        settings = self.cassandra_connection.settings_dict
        settings["OPTIONS"]["connection"] = {"consistency": ConsistencyLevel.ALL}
        connection = CassandraConnection("def_consistency", **settings)
        self.assertEqual(
            connection.session.default_consistency_level, ConsistencyLevel.ALL
        )

    def test_raw_cql_cursor_queries(self):
        cursor = self.connection.cursor()
        self.assertEqual(
            cursor.execute("SELECT count(*) from example_model")[0]["count"], 0
        )

        cursor.execute("INSERT INTO example_model (id) VALUES (1)")

        self.assertEqual(
            cursor.execute("SELECT count(*) from example_model")[0]["count"], 1
        )
