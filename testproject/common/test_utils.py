from django.test import TestCase
from django.core.management import call_command
from django_cassandra_engine.utils import get_cassandra_connections


class CassandraTestCase(TestCase):

    def setUp(self):
        for alias, _ in get_cassandra_connections():
            # Flush the database
            call_command('flush', verbosity=0, interactive=False,
                         database=alias, skip_checks=True,
                         reset_sequences=False,
                         allow_cascade=False,
                         inhibit_post_migrate=True)
