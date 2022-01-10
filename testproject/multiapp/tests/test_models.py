from datetime import datetime

from django.db import connections

from django_cassandra_engine.test import TestCase
from multiapp.models import (
    TestModel,
    TestModel2,
    TestModel3,
)


class ModelsTestCase(TestCase):
    def test_check_if_test_model_synced(self):

        now = datetime(2010, 1, 1, 1, 1)
        TestModel.objects.create(id=1, created_at=now)

        self.assertEqual(TestModel.objects.count(), 1)

        obj = TestModel.objects.all()[0]
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.created_at, now)

    def test_check_if_test_model2_synced(self):

        TestModel2.objects.create(id=11)
        self.assertEqual(TestModel2.objects.count(), 1)
        obj = TestModel2.objects.all()[0]
        self.assertEqual(obj.id, 11)

    def test_check_if_test_model3_synced(self):

        self.assertEqual(TestModel3.__keyspace__, "test_db2")
        TestModel3.objects.create(id=11)
        self.assertEqual(TestModel3.objects.count(), 1)
        obj = TestModel3.objects.all()[0]
        self.assertEqual(obj.id, 11)

    def test_check_if_test_model_saved_to_db_keyspace(self):

        now = datetime(2010, 1, 1, 1, 1)
        obj_id = 123456
        TestModel.objects.create(id=obj_id, created_at=now)

        connection = connections["cassandra"]
        session = connection.connection.session
        session.set_keyspace("test_db")
        self.assertEqual(session.execute("SELECT id FROM test_model")[0]["id"], obj_id)

    def test_check_if_test_model2_saved_to_db2_keyspace(self):

        obj_id = 123456
        TestModel2.objects.create(id=obj_id)

        connection = connections["cassandra"]
        session = connection.connection.session
        session.set_keyspace("test_db2")
        self.assertEqual(session.execute("SELECT id FROM test_model2")[0]["id"], obj_id)

    def test_truncate_models_before_running_tests_works(self):

        self.assertEqual(TestModel.objects.count(), 0)
        self.assertEqual(TestModel2.objects.count(), 0)
        self.assertEqual(TestModel3.objects.count(), 0)
