from optparse import make_option

from django.core.management.base import NoArgsCommand, CommandError
from django.db import connections
from django.conf import settings

from cassandra.cqlengine.management import (
    create_keyspace_simple,
    create_keyspace_network_topology,
    sync_table
)
from django_cassandra_engine.utils import get_engine_from_db_alias


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--database', action='store', dest='database',
                    default=None, help='Nominates a database to synchronize.'),
    )

    help = 'Sync Cassandra database(s)'

    @staticmethod
    def _import_management():
        """
        Import the 'management' module within each installed app, to register
        dispatcher events.
        """

        from importlib import import_module

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

    def sync(self, alias):
        engine = get_engine_from_db_alias(alias)

        if engine != 'django_cassandra_engine':
            raise CommandError('Database {} is not cassandra!'.format(alias))

        connection = connections[alias]
        connection.connect()
        options = connection.settings_dict.get('OPTIONS', {})
        keyspace = connection.settings_dict['NAME']
        replication_opts = options.get('replication', {})
        strategy_class = replication_opts.pop('strategy_class',
                                              'SimpleStrategy')
        replication_factor = replication_opts.pop('replication_factor', 1)

        self.stdout.write('Creating keyspace {}..'.format(keyspace))

        if strategy_class == 'SimpleStrategy':
            create_keyspace_simple(keyspace, replication_factor)
        else:
            create_keyspace_network_topology(keyspace, replication_opts)

        for app_name, app_models \
                in connection.introspection.cql_models.items():
            for model in app_models:
                self.stdout.write('Syncing %s.%s' % (app_name, model.__name__))
                sync_table(model)

    def handle_noargs(self, **options):

        self._import_management()

        database = options.get('database')
        if database is not None:
            return self.sync(database)

        cassandra_alias = None
        for alias in connections:
            engine = get_engine_from_db_alias(alias)
            if engine == 'django_cassandra_engine':
                self.sync(alias)
                cassandra_alias = alias

        if cassandra_alias is None:
            raise CommandError(
                'Please add django_cassandra_engine backend to DATABASES!')
