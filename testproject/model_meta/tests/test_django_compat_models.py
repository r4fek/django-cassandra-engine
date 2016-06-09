import uuid

from django import test

from model_meta.models import CassandraThing, CassandraThingMultiplePK
from django_cassandra_engine.models import (
    ReadOnlyDjangoCassandraQuerySet, DjangoCassandraQuerySet
)


class TestDjangoCompatModel(test.SimpleTestCase):

    model = CassandraThing

    def test_default_manager_is_set(self):
        self.assertTrue(
            isinstance(self.model._default_manager, type(self.model.objects))
        )
        self.assertTrue(
            isinstance(self.model._base_manager, type(self.model.objects))
        )
        self.assertTrue(hasattr(self.model._default_manager, 'all'))
        self.assertTrue(hasattr(self.model._default_manager, 'filter'))

    def test_manager_has_a_name(self):
        self.assertEqual(self.model._default_manager.name, 'objects')

    def test_can_migrate(self):
        self.assertFalse(self.model._meta.can_migrate(connection=None))

    def test_get_all_related_objects_with_model(self):
        self.assertEqual(
            self.model._meta.get_all_related_objects_with_model(),
            []
        )

    def test_pk_attribute(self):
        self.assertEqual(self.model._meta.pk, self.model._meta.get_field('id'))

    def test_get_fields(self):
        expected_field_names = ['id', 'data_abstract']
        fields = self.model._meta._get_fields()
        self.assertEqual(len(fields), len(expected_field_names))
        self.assertEqual([f.name for f in fields], expected_field_names)

    def test_fields_have_attributes_for_django(self):
        fields = self.model._meta._get_fields()

        for field in fields:
            self.assertEqual(field.name, field.db_field_name)
            self.assertEqual(field.field, field)
            self.assertEqual(field.model, self.model)
            self.assertEqual(field.related_query_name(), None)
            self.assertEqual(field.auto_created, False)
            self.assertEqual(field.is_relation, False)
            self.assertEqual(field.remote_field, None)

    def test_meta_attrs(self):
        self.assertEqual(self.model._meta.model_name, 'cassandrathing')
        self.assertEqual(self.model._meta.swappable, False)
        self.assertEqual(self.model._meta.managed, False)

    def test_values_list_with_id_pk_field_returns_it(self):
        some_uuid = uuid.uuid4()
        CassandraThing.objects.create(
            id=some_uuid,
            data_abstract='Some data',
        )

        all_things = CassandraThing.objects.filter(id=some_uuid)

        self.assertEqual(
            list(all_things.values_list('id', flat=True)), [some_uuid]
        )

    def test_values_list_with_pk_returns_the_primary_key_field_uuid(self):
        some_uuid = uuid.uuid4()
        CassandraThing.objects.create(
            id=some_uuid,
            data_abstract='Some data',
        )

        all_things = CassandraThing.objects.filter(id=some_uuid)

        self.assertEqual(
            list(all_things.values_list('pk', flat=True)), [some_uuid]
        )

    def test_values_list_with_pk_can_return_multiple_pks(self):
        some_uuid = uuid.uuid4()
        another_uuid = uuid.uuid4()
        CassandraThingMultiplePK.objects.create(
            id=some_uuid,
            another_id=another_uuid,
            data_abstract='Some data',
        )

        all_things = CassandraThingMultiplePK.objects.filter(
            id=some_uuid,
            another_id=another_uuid,
        )

        self.assertEqual(
            list(all_things.values_list('pk')), [[some_uuid, another_uuid]]
        )

    def test_virtual_fields_are_set(self):
        virtual_fields = [f.name for f in self.model._meta.virtual_fields]
        self.assertEqual(virtual_fields, ['id', 'data_abstract'])

    def test_get_by_pk_queries_using_the_first_pk_in_defined_columns(self):
        some_uuid = uuid.uuid4()
        CassandraThingMultiplePK.objects.create(
            id=some_uuid,
            another_id=uuid.uuid4(),
            data_abstract='Some data',
        )
        self.assertIsNotNone(CassandraThingMultiplePK.objects.get(pk=some_uuid))


class TestReadOnlyDjangoCassandraQuerySet(test.SimpleTestCase):
    def setUp(self):
        self.thing = CassandraThing.objects.create(
            id=uuid.uuid4(),
            data_abstract='Some data',
        )
        self.thing2 = CassandraThing.objects.create(
            id=uuid.uuid4(),
            data_abstract='Some data2',
        )
        self.queryset = ReadOnlyDjangoCassandraQuerySet(
            data=[self.thing, self.thing2], model_class=CassandraThing)

    def test_non_implemented_fields_raise_exception_when_called(self):
        methods_expected_to_raise = []

        for method in methods_expected_to_raise:
            self.assertRaises(ValueError, getattr(self.queryset, method))

    def test_count(self):
        self.assertEqual(self.queryset.count(), 2)

    def test_first(self):
        self.assertEqual(self.queryset.first(), self.thing)

    def test_all(self):
        self.assertEqual(self.queryset.all(), self.queryset)

    def test_objects(self):
        self.assertEqual(self.queryset.objects, self.queryset)

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
        vals = self.queryset.values_list('pk', flat=True)
        self.assertEqual(vals, expected_vals)

    def test_values_list_flat_with_pk_and_exact_pk_field(self):
        expected_vals = [self.thing.id, self.thing2.id]
        vals = self.queryset.values_list('pk', 'id', flat=True)
        self.assertEqual(vals, expected_vals)


class TestDjangoCassandraQuerySet(test.SimpleTestCase):
    def setUp(self):
        self.thing = CassandraThing.objects.create(
            id=uuid.uuid4(),
            data_abstract='Some data',
        )
        self.thing2 = CassandraThing.objects.create(
            id=uuid.uuid4(),
            data_abstract='Some data2',
        )
        self.queryset = CassandraThing.objects.all()

    def tearDown(self):
        CassandraThing.objects.filter(
            id__in=[self.thing.id, self.thing2.id]).delete()

    def test_order_by_data_abstract(self):
        expected_vals = [self.thing, self.thing2]
        vals = list(self.queryset.order_by('data_abstract'))
        self.assertEqual(vals, expected_vals)

    def test_order_by_data_abstract_reversed(self):
        expected_vals = [self.thing2, self.thing]
        vals = list(self.queryset.order_by('-data_abstract'))
        self.assertEqual(vals, expected_vals)
