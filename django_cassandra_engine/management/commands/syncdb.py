import django
from django.conf import settings
from django.core.management.commands.syncdb import Command as SyncCommand
from django.db import connections

from cqlengine.management import create_keyspace, sync_table


class Command(SyncCommand):

    @staticmethod
    def _import_management():
        """
        Import the 'management' module within each installed app, to register
        dispatcher events.
        """

        from django.utils.importlib import import_module

        for app_name in settings.INSTALLED_APPS:
            try:
                import_module('.management', app_name)
            except ImportError as exc:
                # This is slightly hackish. We want to ignore ImportErrors
                # if the "management" module itself is missing -- but we don't
                # want to ignore the exception if the management module exists
                # but raises an ImportError for some reason. The only way we
                # can do this is to check the text of the exception. Note that
                # we're a bit broad in how we check the text, because different
                # Python implementations may not use the same text.
                # CPython uses the text "No module named management"
                # PyPy uses "No module named myproject.myapp.management"
                msg = exc.args[0]
                if not msg.startswith('No module named') \
                        or 'management' not in msg:
                    raise

    def handle_noargs(self, **options):
        db = options.get('database')
        engine = settings.DATABASES.get(db, {}).get('ENGINE', '')

        # Call regular syncdb if engine is different from ours
        if engine != 'django_cassandra_engine':
            return super(Command, self).handle_noargs(**options)

        if django.VERSION < (1, 7):
            self._import_management()

        connection = connections[db]
        connection.connect()
        options = connection.settings_dict.get('OPTIONS', {})
        replication_opts = options.get('replication', {})
        keyspace = connection.settings_dict['NAME']

        self.stdout.write('Creating keyspace %s..' % keyspace)
        create_keyspace(keyspace, **replication_opts)
        for app_name, app_models \
                in connection.introspection.cql_models.iteritems():

            for model in app_models:
                self.stdout.write('Syncing %s.%s' % (app_name, model.__name__))
                sync_table(model, create_missing_keyspace=False)
