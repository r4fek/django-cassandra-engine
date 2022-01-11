from datetime import datetime
from http import client
from unittest import skipIf
import uuid

from django.urls import reverse
from rest_framework.test import APITestCase

from common.models import (
    CassandraFamilyMember,
    CassandraThing,
    CassandraThingMultiplePK,
)
from common.serializers import CassandraFamilyMemberSerializer
from django_cassandra_engine.test import TestCase as CassandraTestCase


class TestModelViewSet(APITestCase):

    url = "/common/thing-modelviewset/"

    def setUp(self):
        self.data2a = {
            "id": "a9be910b-3338-4340-b773-f7ec2bc1ce1a",
            "data_abstract": "TeXt",
        }
        self.data2b = {
            "id": "a9be910b-3338-4340-b773-f7ec2bc1ce1b",
            "data_abstract": "TeXt",
        }

    def test_create_thing2a(self):
        response = self.client.post(self.url, self.data2a, format="json")
        self.assertEqual(response.status_code, client.CREATED)
        self.assertEqual(CassandraThing.objects.count(), 1)
        self.assertEqual(CassandraThing.objects.get().id, uuid.UUID(self.data2a["id"]))
        get_url = "{}{}/".format(self.url, self.data2a["id"])
        response = self.client.get(get_url, format="json")
        self.assertDictEqual(response.json(), self.data2a)
        self.assertEqual(response.status_code, client.OK)

    def test_create_thing2b(self):
        response = self.client.post(self.url, self.data2b, format="json")
        self.assertEqual(response.status_code, client.CREATED)
        self.assertEqual(CassandraThing.objects.count(), 1)

        self.assertEqual(
            CassandraThing.objects.get(id=self.data2b["id"]).id,
            uuid.UUID(self.data2b["id"]),
        )

        get_url = "{}{}/".format(self.url, self.data2b["id"])
        response = self.client.get(get_url, format="json")
        self.assertDictEqual(response.json(), self.data2b)
        self.assertEqual(response.status_code, client.OK)


class TestListCreateAPIViewWithMultiplePK(APITestCase):
    def setUp(self):
        self.data = {
            "id": "a9be910b-3338-4340-b773-f7ec2bc1ce1a",
            "another_id": "a9be910b-3338-4340-b773-f7ec2bc1ce1b",
            "data_abstract": "TeXt",
            "created_on": "2016-11-12T23:12",
        }

    def test_create_multiple_pk_thing(self):
        url = reverse("thing_listcreate_api")
        response = self.client.post(url, self.data)
        expected_json = {
            "another_id": "a9be910b-3338-4340-b773-f7ec2bc1ce1b",
            "created_on": "2016-11-12T23:12:00Z",
            "data_abstract": "TeXt",
            "id": "a9be910b-3338-4340-b773-f7ec2bc1ce1a",
        }
        self.assertEqual(response.status_code, client.CREATED)
        self.assertDictEqual(response.json(), expected_json)

        model = CassandraThingMultiplePK.objects.get(id=self.data["id"])

        self.assertEqual(str(model.id), self.data["id"])
        self.assertEqual(str(model.another_id), self.data["another_id"])
        self.assertEqual(model.data_abstract, self.data["data_abstract"])


class TestSerializer(APITestCase, CassandraTestCase):
    def test_serialize_creates(self):
        now = datetime.now()
        data = {
            "id": str(uuid.uuid4()),
            "first_name": "Homer",
            "last_name": "Simpson",
            "is_real": True,
            "favourite_number": 10,
            "favourite_float_number": float(10.10),
            "created_on": now,
        }
        serializer = CassandraFamilyMemberSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        self.assertEqual(CassandraFamilyMember.objects.all().count(), 1)
        model = CassandraFamilyMember.objects.all()[0]
        self.assertEqual(model.first_name, "Homer")
        self.assertEqual(model.last_name, "Simpson")
        self.assertEqual(model.is_real, True)
        self.assertEqual(model.favourite_number, 10)
        self.assertEqual(model.id, uuid.UUID(data["id"]))
