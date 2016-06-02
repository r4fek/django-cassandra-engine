import uuid
from datetime import datetime

from django import test
from cassandra.cqlengine.query import QueryException
from django_cassandra_engine.utils import get_cassandra_connections
from django.core.management.base import CommandError
from django.core.management import call_command

from common.models import CassandraThingWithDate, CassandraThingMultiplePK


class TestDjangoCassandraQuerySet(test.SimpleTestCase):
    def setUp(self):
        self.thing = CassandraThingWithDate.objects.create(
            id=uuid.uuid4(),
            created_on=datetime(2015, 6, 10),
        )
        self.thing2 = CassandraThingWithDate.objects.create(
            id=uuid.uuid4(),
            created_on=datetime(2016, 6, 10),
        )
        self.queryset = CassandraThingWithDate.objects.order_by(
            'created_on')

    def tearDown(self):
        for alias, _ in get_cassandra_connections():
            # Flush the database
            try:
                call_command(
                    'flush', verbosity=0, interactive=False,
                    database=alias, skip_checks=True,
                    reset_sequences=False,
                    allow_cascade=False,
                    load_initial_data=False,
                    inhibit_post_migrate=True,
                    inhibit_post_syncdb=True
                )
            except CommandError:
                pass

    def test_non_implemented_fields_raise_exception_when_called(self):
        methods_expected_to_raise = []

        for method in methods_expected_to_raise:
            self.assertRaises(ValueError, getattr(self.queryset, method))

    def test_count(self):
        self.assertEqual(self.queryset.count(), 2)

    def test_first(self):
        self.assertEqual(
            CassandraThingWithDate.objects.order_by('created_on').first(),
            self.thing
        )

    def test_all(self):
        self.assertEqual(self.queryset.all(), self.queryset)

    def test_values_list_with_pk_field_specified_exactly(self):
        expected_vals = [[self.thing.id], [self.thing2.id]]
        vals = self.queryset.values_list('id')
        self.assertEqual(vals, expected_vals)

    def test_values_list_flat_with_pk_field_specified_exactly(self):
        expected_vals = [self.thing.id, self.thing2.id]
        vals = self.queryset.values_list('id', flat=True)
        self.assertEqual(vals, expected_vals)

    def test_values_list_with_pk(self):
        expected_vals = [[self.thing.id], [self.thing2.id]]
        vals = self.queryset.values_list('pk')
        self.assertEqual(vals, expected_vals)

    def test_values_list_flat_with_pk(self):
        expected_vals = [self.thing.id, self.thing2.id]
        vals = list(self.queryset.values_list('pk', flat=True))
        self.assertEqual(vals, expected_vals)

    def test_values_list_flat_with_pk_and_exact_pk_field(self):
        expected_vals = [self.thing.id, self.thing2.id]
        vals = list(self.queryset.values_list('pk', 'id', flat=True))
        self.assertEqual(vals, expected_vals)

    def test_order_by_created_on_ascending(self):
        expected_vals = [self.thing, self.thing2]
        vals = list(CassandraThingWithDate.objects.order_by('created_on'))
        self.assertEqual(vals, expected_vals)

    def test_order_by_created_on_descending(self):
        expected_vals = [self.thing2, self.thing]
        vals = list(CassandraThingWithDate.objects.order_by('-created_on'))
        self.assertEqual(vals, expected_vals)

    def test_order_by_unknown_column_raises_exception(self):
        with self.assertRaises(QueryException):
            CassandraThingWithDate.objects.order_by('unknown', 'also_unkown')

    def test_order_by_with_fallback_off_raises(self):
        queryset = CassandraThingWithDate.objects
        queryset._USE_FALLBACK_ORDER_BY = False
        with self.assertRaises(QueryException):
            queryset.order_by('created_on')

    def test_order_by_on_second_primary_key_with_fallback_disabled(self):
        queryset = CassandraThingMultiplePK.objects
        queryset._USE_FALLBACK_ORDER_BY = False
        assert queryset.order_by('another_id') is not None
