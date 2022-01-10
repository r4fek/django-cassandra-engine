from datetime import datetime
import uuid

from cassandra.cqlengine.query import QueryException
from django import test
from django.conf import settings

from common.models import CassandraThingMultiplePK


class TestDjangoCassandraQuerySet(test.SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        cls.thing = CassandraThingMultiplePK.objects.create(
            id=uuid.uuid4(),
            created_on=datetime(2015, 6, 10),
        )
        cls.thing2 = CassandraThingMultiplePK.objects.create(
            id=uuid.uuid4(),
            created_on=datetime(2016, 6, 10),
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def get_queryset(self):
        return CassandraThingMultiplePK.objects.all()

    def get_queryset_ordered(self):
        return CassandraThingMultiplePK.objects.all().order_by("created_on")

    def test_exists(self):
        queryset_with_items = CassandraThingMultiplePK.objects.all()
        self.assertTrue(queryset_with_items.exists())

        unknown_id = uuid.uuid4()
        queryset_empty = CassandraThingMultiplePK.objects.filter(id=unknown_id)
        self.assertFalse(queryset_empty.exists())

    def test_non_implemented_fields_raise_exception_when_called(self):
        methods_expected_to_raise = []

        for method in methods_expected_to_raise:
            self.assertRaises(ValueError, getattr(self.get_queryset(), method))

    def test_count(self):
        self.assertEqual(self.get_queryset().count(), 2)

    def test_first(self):
        self.assertEqual(
            CassandraThingMultiplePK.objects.order_by("created_on").first(), self.thing
        )

    def test_all(self):
        self.assertEqual(self.get_queryset().all(), self.get_queryset())

    def test_values_list_with_pk_field_specified_exactly(self):
        expected_vals = [[self.thing.id], [self.thing2.id]]
        vals = list(self.get_queryset_ordered().values_list("id"))
        self.assertEqual(vals, expected_vals)

    def test_values_list_flat_with_pk_field_specified_exactly(self):
        expected_vals = [self.thing.id, self.thing2.id]
        vals = list(self.get_queryset_ordered().values_list("id", flat=True))
        self.assertEqual(vals, expected_vals)

    def test_values_list_with_pk(self):
        expected_vals = [
            [self.thing.id, self.thing.another_id],
            [self.thing2.id, self.thing2.another_id],
        ]
        vals = list(self.get_queryset_ordered().values_list("pk"))
        self.assertEqual(vals, expected_vals)

    def test_values_list_flat_with_pk(self):
        expected_vals = [
            self.thing.id,
            self.thing.another_id,
            self.thing2.id,
            self.thing2.another_id,
        ]
        vals = list(self.get_queryset_ordered().values_list("pk", flat=True))
        self.assertEqual(vals, expected_vals)

    def test_values_list_flat_with_pk_and_exact_pk_field(self):
        expected_vals = [
            self.thing.id,
            self.thing.another_id,
            self.thing2.id,
            self.thing2.another_id,
        ]
        vals = list(self.get_queryset_ordered().values_list("pk", "id", flat=True))
        self.assertEqual(vals, expected_vals)

    def test_order_by_created_on_ascending(self):
        expected_vals = [self.thing, self.thing2]
        vals = list(CassandraThingMultiplePK.objects.order_by("created_on"))
        self.assertEqual(vals, expected_vals)

    def test_order_by_created_on_descending(self):
        expected_vals = [self.thing2, self.thing]
        vals = list(CassandraThingMultiplePK.objects.order_by("-created_on"))
        self.assertEqual(vals, expected_vals)

    def test_order_by_unknown_column_raises_exception(self):
        with self.assertRaises(QueryException):
            CassandraThingMultiplePK.objects.order_by("unknown", "also_known")

    def test_order_by_with_fallback_off_raises(self):
        queryset = CassandraThingMultiplePK.objects
        orig_setting = settings.CASSANDRA_FALLBACK_ORDER_BY_PYTHON
        settings.CASSANDRA_FALLBACK_ORDER_BY_PYTHON = False
        with self.assertRaises(QueryException):
            queryset.order_by("created_on")
        settings.CASSANDRA_FALLBACK_ORDER_BY_PYTHON = orig_setting

    def test_order_by_on_second_primary_key_with_fallback_disabled(self):
        queryset = CassandraThingMultiplePK.objects
        queryset._USE_FALLBACK_ORDER_BY = False
        assert queryset.order_by("another_id") is not None
