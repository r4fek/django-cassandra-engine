from datetime import datetime

from django.core.management.sql import sql_flush
from mock import Mock

from django_cassandra_engine.test import TestCase
from django_cassandra_engine.connection import CassandraConnection
from django_cassandra_engine.utils import (
    get_cql_models,
    get_installed_apps,
    get_cassandra_connection
)
from app.models import ExampleModel, ExampleModel2


class DatabaseWrapperTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(DatabaseWrapperTestCase, cls).setUpClass()
        cls.connection = get_cassandra_connection()
        cls.all_models = []
        apps = get_installed_apps()
        for app in apps:
            cls.all_models.extend(get_cql_models(app))

        cls.all_django_tables = \
            [model.column_family_name(include_keyspace=False)
             for model in cls.all_models]

    def test_auto_connect(self):

        self.assertIsNotNone(self.connection.connection)
        self.assertTrue(self.connection.connected)
        self.assertIsInstance(self.connection.connection, CassandraConnection)

    def test_sql_flush_works(self):

        mock_style = Mock()
        ExampleModel.objects.create(id='1', created_at=datetime.now(),
                                    deleted=False)
        ExampleModel2.objects.create(id='3')

        self.assertEqual(ExampleModel.objects.count(), 1)
        self.assertEqual(ExampleModel2.objects.count(), 1)

        statements = sql_flush(mock_style, self.connection)
        self.assertEqual(statements, [])
        self.assertEqual(ExampleModel.objects.count(), 0)
        self.assertEqual(ExampleModel2.objects.count(), 0)

    def test_connection_introspection_table_names(self):

        tables = self.connection.introspection.table_names()

        self.assertEqual(set(tables), set(self.all_django_tables))

    def test_connection_introspection_django_table_names(self):

        self.assertEqual(
            set(self.connection.introspection.django_table_names()),
            set(self.all_django_tables))

    def test_connection_introspection_sequence_list(self):

        self.assertEqual(self.connection.introspection.sequence_list(), [])
