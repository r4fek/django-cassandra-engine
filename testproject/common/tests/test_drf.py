import uuid
import six.moves.http_client

from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

from common.models import CassandraThing


class TestModelViewSet(APITestCase):

    url = '/common/thing-modelviewset/'

    def setUp(self):
        self.data2a = {
            'id': 'a9be910b-3338-4340-b773-f7ec2bc1ce1a',
            'data_abstract': 'TeXt'
        }
        self.data2b = {
            'id': 'a9be910b-3338-4340-b773-f7ec2bc1ce1b',
            'data_abstract': 'TeXt'
        }

    def test_create_thing2a(self):
        response = self.client.post(self.url, self.data2a, format='json')
        self.assertEqual(response.status_code, six.moves.http_client.CREATED)
        self.assertEqual(CassandraThing.objects.count(), 1)
        self.assertEqual(
            CassandraThing.objects.get().id,
            uuid.UUID(self.data2a['id'])
        )
        get_url = '{}{}/'.format(self.url, self.data2a['id'])
        response = self.client.get(get_url, format='json')
        self.assertDictEqual(response.json(), self.data2a)
        self.assertEqual(response.status_code, six.moves.http_client.OK)

    def test_create_thing2b(self):
        response = self.client.post(self.url, self.data2b, format='json')
        self.assertEqual(response.status_code, six.moves.http_client.CREATED)
        self.assertEqual(CassandraThing.objects.count(), 2)

        self.assertEqual(
            CassandraThing.objects.get(id=self.data2b['id']).id,
            uuid.UUID(self.data2b['id'])
        )

        get_url = '{}{}/'.format(self.url, self.data2b['id'])
        response = self.client.get(get_url, format='json')
        self.assertDictEqual(response.json(), self.data2b)
        self.assertEqual(response.status_code, six.moves.http_client.OK)


class CreateThingMultiplePKTest(APITestCase):
    def setUp(self):
        self.data = {
            'id': 'a9be910b-3338-4340-b773-f7ec2bc1ce1a',
            'another_id': 'a9be910b-3338-4340-b773-f7ec2bc1ce1b',
            'data_abstract': 'TeXt',
            'created_on': '2016-11-12T23:12'
        }

    def test_create_multiple_pk_thing(self):
        url = reverse('thing_listcreate_api')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, 201)
