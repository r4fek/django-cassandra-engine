from django import test

from model_meta.models import Relation, CassandraThing


class TestModelManager(test.SimpleTestCase):

    MODELS_TO_TEST = (CassandraThing, Relation)

    def test_default_manager_is_set(self):
        for model in self.MODELS_TO_TEST:
            self.assertTrue(
                isinstance(model._default_manager, type(model.objects))
            )
            self.assertTrue(hasattr(model._default_manager, 'all'))
            self.assertTrue(hasattr(model._default_manager, 'filter'))

    def test_manager_has_a_name(self):
        for model in self.MODELS_TO_TEST:
            self.assertEqual(model._default_manager.name, 'objects')
