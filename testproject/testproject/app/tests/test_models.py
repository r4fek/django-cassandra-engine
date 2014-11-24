from datetime import datetime

from django.test import TestCase
from mock import patch

from testproject.app.models import ExampleModel


class ModelsTestCase(TestCase):

    def test_check_if_model_synced(self):

        now = datetime(2010, 1, 1, 1, 1)
        ExampleModel.objects.create(id=1, created_at=now)

        self.assertEqual(ExampleModel.objects.count(), 1)

        obj = ExampleModel.objects.all()[0]
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.created_at, now)
