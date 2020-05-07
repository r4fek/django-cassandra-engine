from datetime import datetime

from six.moves import http_client

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from freezegun import freeze_time

from django_cassandra_engine.test import TestCase as CassandraTestCase
from common.models import CassandraThingMultiplePK


@freeze_time('14-06-15 15:44:25')
def create_thing():
    return CassandraThingMultiplePK.objects.create(created_on=datetime.now())


@freeze_time('14-06-15 15:44:25')
class TestViewSet(CassandraTestCase):
    def test_get_when_no_records_exist(self):
        response = self.client.get(reverse('thing_viewset_api'))
        self.assertEqual(response.status_code, http_client.OK)
        self.assertEqual(response.json(), [])

    def test_get(self):
        thing = create_thing()

        response = self.client.get(reverse('thing_viewset_api'))
        self.assertEqual(response.status_code, http_client.OK)

        expected_response = [
            {
                'created_on': '2015-06-14T15:44:25Z',
                'data_abstract': None,
                'another_id': str(thing.another_id),
                'id': str(thing.id),
            }
        ]
        self.assertEqual(response.json(), expected_response)


@freeze_time('14-06-15 15:44:25')
class TestListCreateAPIView(CassandraTestCase):
    def test_get_when_no_records_exist(self):
        response = self.client.get(reverse('thing_listcreate_api'))
        self.assertEqual(response.status_code, http_client.OK)
        self.assertEqual(response.json(), [])

    def test_post(self):
        response = self.client.post(
            reverse('thing_listcreate_api'),
            {'created_on': '2015-06-14T15:44:25Z'},
        )
        self.assertEqual(response.status_code, http_client.CREATED)
        assert CassandraThingMultiplePK.objects.all().count() == 1


@freeze_time('14-06-15 15:44:25')
class TestListAPIView(CassandraTestCase):
    def test_get(self):
        thing = create_thing()
        response = self.client.get(reverse('thing_listview_api'))
        self.assertEqual(response.status_code, http_client.OK)

        expected_response = [
            {
                'created_on': '2015-06-14T15:44:25Z',
                'data_abstract': None,
                'another_id': str(thing.another_id),
                'id': str(thing.id),
            }
        ]
        self.assertEqual(response.json(), expected_response)
