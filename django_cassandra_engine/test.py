from django.core.management import call_command
from django.test import TestCase as DjangoTestCase

from django_cassandra_engine.utils import get_cassandra_connections


class TestCase(DjangoTestCase):
    def _fixture_teardown(self):
        """
        Allow normal django TestCase fixture teardown, but also flush the test
        database for each cassandra alias.
        """
        super(TestCase, self)._fixture_teardown()

        for alias, _ in get_cassandra_connections():
            # Flush the database
            call_command('flush', verbosity=0, interactive=False,
                         database=alias, skip_checks=True,
                         reset_sequences=False,
                         allow_cascade=False,
                         load_initial_data=False,
                         inhibit_post_migrate=True,
                         inhibit_post_syncdb=True)
