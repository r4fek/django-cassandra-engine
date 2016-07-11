import uuid

from rest_framework.test import APITestCase

from common.models import CassandraThing


class CreateReadThingTest(APITestCase):

    def setUp(self):
        self.data2a = {'id': 'a9be910b-3338-4340-b773-f7ec2bc1ce1a', 'data_abstract': 'TeXt'}
        self.data2b = {'id': 'a9be910b-3338-4340-b773-f7ec2bc1ce1b', 'data_abstract': 'TeXt'}

    def test_create_thing2a(self):
        response = self.client.post('/common/thing-modelviewset/', self.data2a, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CassandraThing.objects.count(), 1)
        self.assertEqual(CassandraThing.objects.get().id, uuid.UUID('a9be910b-3338-4340-b773-f7ec2bc1ce1a'))

    def test_create_thing2b(self):
        response = self.client.post('/common/thing-modelviewset/', self.data2b, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CassandraThing.objects.count(), 2)
        self.assertEqual(CassandraThing.objects.get(id='a9be910b-3338-4340-b773-f7ec2bc1ce1b').id,
                         uuid.UUID('a9be910b-3338-4340-b773-f7ec2bc1ce1b'))
        response = self.client.get('/api/thing-modelviewset4/a9be910b-3338-4340-b773-f7ec2bc1ce1b/', format='json')
        self.assertEqual(response.status_code, 200)


class CreateThingMultiplePKTest(APITestCase):
    def setUp(self):
        self.data = {'id': 'a9be910b-3338-4340-b773-f7ec2bc1ce1a', 'another_id': 'a9be910b-3338-4340-b773-f7ec2bc1ce1b',
                     'data_abstract': 'TeXt', 'created_on': '2016-11-12T23:12'}

    def test_create_multiple_pk_thing(self):
        response = self.client.post('/common/thing-listcreate/', self.data)
        self.assertEqual(response.status_code, 201)
