from django import test

from model_meta.models import CassandraThing


class TestModelManager(test.SimpleTestCase):

    model = CassandraThing

    def test_default_manager_is_set(self):
        self.assertTrue(
            isinstance(self.model._default_manager, type(self.model.objects))
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
