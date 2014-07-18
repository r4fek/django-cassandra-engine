from optparse import make_option

from cqlengine.management import create_keyspace, sync_table

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.db import DEFAULT_DB_ALIAS, connections, models
from django.utils.importlib import import_module

from django_cassandra_engine.utils import get_cql_models


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS,
            help='Nominates a database to synchronize. '
                 'Defaults to the "default" database.'),
    )
    help = "Create the database tables for all apps in INSTALLED_APPS " \
           "whose tables haven't already been created."

    def handle_noargs(self, **options):
        # Import the 'management' module within each installed app, to register
        # dispatcher events.
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

        db = options.get('database')
        connection = connections[db]
        connection.connect()
        options = connection.settings_dict.get('OPTIONS', {})
        replication_opts = options.get('replication', {})
        keyspace = connection.settings_dict['NAME']

        self.stdout.write('Creating keyspace %s..' % keyspace)
        create_keyspace(keyspace, **replication_opts)

        apps = models.get_apps()
        for app in apps:
            app_models = get_cql_models(app)
            for model in app_models:
                self.stdout.write('Syncing %s.%s' %
                                  (app.__name__, model.__name__))
                sync_table(model, create_missing_keyspace=False)
