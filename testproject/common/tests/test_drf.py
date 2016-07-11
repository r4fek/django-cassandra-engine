from rest_framework.test import APITestCase

from common.models import CassandraThing


class CreateReadThingTest1(APITestCase):

    def setUp(self):
        self.data = {'id': 'a9be910b-3338-4340-b773-f7ec2bc1ce1a', 'data_abstract': 'TeXt'}

    def test_create_thing2(self):
        response = self.client.post('/common/thing-modelviewset/', self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CassandraThing.objects.count(), 1)
        self.assertEqual(CassandraThing.objects.get().id, 'a9be910b-3338-4340-b773-f7ec2bc1ce1a')


class CreateReadThingTest2(APITestCase):

    def setUp(self):
        self.data = {'id': 'a9be910b-3338-4340-b773-f7ec2bc1ce1b', 'data_abstract': 'TeXt'}

    def test_create_thing2(self):
        response = self.client.post('/common/thing-modelviewset/', self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CassandraThing.objects.count(), 2)
        self.assertEqual(CassandraThing.objects.get(id='a9be910b-3338-4340-b773-f7ec2bc1ce1b').id, 'a9be910b-3338-4340-b773-f7ec2bc1ce1b')
        response = self.client.get('/common/thing-modelviewset/a9be910b-3338-4340-b773-f7ec2bc1ce1b/', format='json')
        self.assertEqual(response.status_code, 200)
