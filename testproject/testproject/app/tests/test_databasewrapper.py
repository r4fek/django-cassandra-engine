from django.db import connection
from django.test import TestCase
from django_cassandra_engine.connection import CassandraConnection


class DatabaseWrapperTestCase(TestCase):

    def test_auto_connect(self):

        self.assertIsNotNone(connection.connection)
        self.assertTrue(connection.connected)
        self.assertIsInstance(connection.connection, CassandraConnection)
