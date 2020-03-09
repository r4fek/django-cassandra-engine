from django.core.management import call_command
from django.test import TestCase as DjangoTestCase

from django_cassandra_engine.utils import (
    get_cassandra_connections,
    get_cassandra_db_aliases,
)


class TestCase(DjangoTestCase):
    databases = list(get_cassandra_db_aliases())

    def _should_reload_connections(self):
        return False

    def _fixture_teardown(self):
        """
        Allow normal django TestCase fixture teardown, but also flush the test
        database for each cassandra alias.
        """
        super(TestCase, self)._fixture_teardown()

        for alias, _ in get_cassandra_connections():
            # Flush the database
            call_command(
                'flush',
                verbosity=1,
                interactive=False,
                database=alias,
                skip_checks=True,
                reset_sequences=False,
                allow_cascade=False,
                inhibit_post_migrate=True,
            )
