import httplib
from datetime import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from freezegun import freeze_time
from rest_framework.test import APITestCase
from django_cassandra_engine.test import TestCase

from common.models import CassandraThingWithDate


@freeze_time('14-06-15 15:44:25')
def create_thing():
    return CassandraThingWithDate.objects.create(
        created_on=datetime.now()
    )


@freeze_time('14-06-15 15:44:25')
class TestThingViewSet(APITestCase, TestCase):
    def test_getwhen_no_records_exist(self):
        response = self.client.get(reverse('thing_viewset_api'))
        self.assertEqual(response.status_code, httplib.OK)
        self.assertEqual(response.json(), [])

    def test_get(self):
        thing = create_thing()

        response = self.client.get(reverse('thing_viewset_api'))
        self.assertEqual(response.status_code, httplib.OK)

        expected_response = [{
            'created_on': '2015-06-14T15:44:25',
            'id': str(thing.id)}
        ]
        self.assertEqual(response.json(), expected_response)


@freeze_time('14-06-15 15:44:25')
class TestThingListCreateAPIView(APITestCase, TestCase):
    def test_get_when_no_records_exist(self):
        response = self.client.get(reverse('thing_listcreate_api'))
        self.assertEqual(response.status_code, httplib.OK)
        self.assertEqual(response.json(), [])

    def test_post(self):
        response = self.client.post(
            reverse('thing_listcreate_api'),
            {
                'created_on': '2015-06-14T15:44:25'
            }
        )
        self.assertEqual(response.status_code, httplib.CREATED)
        assert CassandraThingWithDate.objects.all().count() == 1


class TestThingListAPIView(APITestCase, TestCase):

    @freeze_time('14-06-15 15:44:25')
    def test_get(self):
        thing = create_thing()
        response = self.client.get(reverse('thing_listview_api'))
        self.assertEqual(response.status_code, httplib.OK)

        expected_response = [{
            'created_on': '2015-06-14T15:44:25',
            'id': str(thing.id)}
        ]
        self.assertEqual(response.json(), expected_response)
