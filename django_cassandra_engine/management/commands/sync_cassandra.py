from django.core.management.base import NoArgsCommand
from django.db import connections

from django_cassandra_engine.management.commands import syncdb


class Command(NoArgsCommand):

    help = 'Sync Cassandra database'

    def handle_noargs(self, **options):
        cassandra_alias = None

        for alias in connections:
            engine = connections[alias].settings_dict.get('ENGINE', '')
            if engine == 'django_cassandra_engine':
                cassandra_alias = alias

        if cassandra_alias is None:
            self.stderr.write(
                'Please add django_cassandra_engine backend to DATABASES!')
            return

        options['database'] = options.get('database', cassandra_alias)
        syncdb.Command().execute(**options)
