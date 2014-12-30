from django.conf import settings
from django.core.management.commands.syncdb import Command as SyncCommand

from django_cassandra_engine.management.commands import sync_cassandra


class Command(SyncCommand):

    def handle_noargs(self, **options):
        db = options.get('database')
        engine = settings.DATABASES.get(db, {}).get('ENGINE', '')

        # Call regular syncdb if engine is different from ours
        if engine != 'django_cassandra_engine':
            return super(Command, self).handle_noargs(**options)
        else:
            return sync_cassandra.Command().execute(**options)
