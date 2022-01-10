from datetime import datetime

from app.models import ExampleModel, ExampleModel2
from django_cassandra_engine.test import TestCase


class ModelsTestCase(TestCase):
    def test_check_if_model_synced(self):

        now = datetime(2010, 1, 1, 1, 1)
        ExampleModel.objects.create(id=1, created_at=now)

        self.assertEqual(ExampleModel.objects.count(), 1)

        obj = ExampleModel.objects.all()[0]
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.created_at, now)

    def test_check_if_model_saved_to_test_keyspace(self):

        now = datetime(2010, 1, 1, 1, 1)
        obj_id = 123456
        obj = ExampleModel.objects.create(id=obj_id, created_at=now)
        self.assertEqual(obj.__keyspace__, "test_db")

        from cassandra.cqlengine.connection import get_session

        session = get_session()
        session.set_keyspace("test_db")
        self.assertEqual(
            session.execute("SELECT id FROM example_model")[0]["id"], obj_id
        )

    def test_truncate_models_before_running_tests_works(self):

        self.assertEqual(ExampleModel.objects.count(), 0)
        self.assertEqual(ExampleModel2.objects.count(), 0)
