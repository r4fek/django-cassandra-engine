from django.core.management import call_command
from django.test import TestCase as DjangoTestCase
from django.db import connections


class TestCase(DjangoTestCase):

    def _databases_names(self, include_mirrors=True):

        cassandra_aliases = []
        for alias in connections:
            if connections[alias].settings_dict['ENGINE'] == \
                    'django_cassandra_engine':
                cassandra_aliases.append(alias)
        return cassandra_aliases

    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        for db_name in self._databases_names(include_mirrors=False):
            # Flush the database
            call_command('flush', verbosity=0, interactive=False,
                         database=db_name, skip_checks=True,
                         reset_sequences=False,
                         allow_cascade=False,
                         inhibit_post_migrate=True,
                         inhibit_post_syncdb=True)
