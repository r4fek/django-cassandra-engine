from optparse import make_option

from django.core.management.base import NoArgsCommand, CommandError
from django.db import connections
from django.conf import settings

from cassandra.cqlengine import management
from cassandra.cqlengine.models import Model
from django.apps import apps
from django.db.models.signals import post_migrate

from django_cassandra_engine.models import DjangoCassandraModel
from django_cassandra_engine.utils import get_engine_from_db_alias


def emit_post_migrate_signal(verbosity, interactive, db):
    # Emit the post_migrate signal for every application.
    for app_config in apps.get_app_configs():
        if app_config.models_module is None:
            continue
        if verbosity >= 2:
            print("Running post-migrate handlers for application %s" % app_config.label)
        post_migrate.send(
            sender=app_config,
            app_config=app_config,
            verbosity=verbosity,
            interactive=interactive,
            using=db)


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
            management.create_keyspace_simple(keyspace, replication_factor)
        else:
            management.create_keyspace_network_topology(keyspace, replication_opts)

        for app_name, app_models \
                in connection.introspection.cql_models.items():
            for model in app_models:
                self.stdout.write('Syncing %s.%s' % (app_name, model.__name__))
                # patch this object used for type check in management.sync_table()
                management.Model = (Model, DjangoCassandraModel)
                management.sync_table(model)

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

        # Send the post_migrate signal, so individual apps can do whatever they need
        # to do at this point.
        emit_post_migrate_signal(1, False, cassandra_alias)
