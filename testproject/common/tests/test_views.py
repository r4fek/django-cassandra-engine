from datetime import datetime

from six.moves import http_client
from django.core.urlresolvers import reverse
from freezegun import freeze_time
from django.test import TestCase
from django.core.management import call_command
from django_cassandra_engine.utils import get_cassandra_connections

from common.models import CassandraThingMultiplePK


@freeze_time('14-06-15 15:44:25')
def create_thing():
    return CassandraThingMultiplePK.objects.create(
        created_on=datetime.now()
    )


class CassandraAPITestCase(TestCase):

    def setUp(self):
        for alias, _ in get_cassandra_connections():
            # Flush the database
            call_command('flush', verbosity=0, interactive=False,
                         database=alias, skip_checks=True,
                         reset_sequences=False,
                         allow_cascade=False,
                         load_initial_data=False,
                         inhibit_post_migrate=True,
                         inhibit_post_syncdb=True)


@freeze_time('14-06-15 15:44:25')
class TestThingViewSet(CassandraAPITestCase):
    def test_getwhen_no_records_exist(self):
        response = self.client.get(reverse('thing_viewset_api'))
        self.assertEqual(response.status_code, http_client.OK)
        self.assertEqual(response.json(), [])

    def test_get(self):
        thing = create_thing()

        response = self.client.get(reverse('thing_viewset_api'))
        self.assertEqual(response.status_code, http_client.OK)

        expected_response = [{
            'created_on': '2015-06-14T15:44:25',
            'data_abstract': None,
            'another_id': str(thing.another_id),
            'id': str(thing.id)}
        ]
        self.assertEqual(response.json(), expected_response)


@freeze_time('14-06-15 15:44:25')
class TestThingListCreateAPIView(CassandraAPITestCase):
    def test_get_when_no_records_exist(self):
        response = self.client.get(reverse('thing_listcreate_api'))
        self.assertEqual(response.status_code, http_client.OK)
        self.assertEqual(response.json(), [])

    def test_post(self):
        response = self.client.post(
            reverse('thing_listcreate_api'),
            {
                'created_on': '2015-06-14T15:44:25'
            }
        )
        self.assertEqual(response.status_code, http_client.CREATED)
        assert CassandraThingMultiplePK.objects.all().count() == 1


class TestThingListAPIView(CassandraAPITestCase):

    @freeze_time('14-06-15 15:44:25')
    def test_get(self):
        thing = create_thing()
        response = self.client.get(reverse('thing_listview_api'))
        self.assertEqual(response.status_code, http_client.OK)

        expected_response = [{
            'created_on': '2015-06-14T15:44:25',
            'data_abstract': None,
            'another_id': str(thing.another_id),
            'id': str(thing.id)}
        ]
        self.assertEqual(response.json(), expected_response)
