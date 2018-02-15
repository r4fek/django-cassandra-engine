from django.core.management.commands.flush import Command as FlushCommand

from django_cassandra_engine.utils import get_engine_from_db_alias


class Command(FlushCommand):

    def handle_noargs(self, **options):
        engine = get_engine_from_db_alias(options['database'])
        if engine == 'django_cassandra_engine':
            options.update({
                'interactive': False,
                'inhibit_post_migrate': True
            })

        return super(Command, self).handle_noargs(**options)

    def handle(self, **options):
        engine = get_engine_from_db_alias(options['database'])
        if engine == 'django_cassandra_engine':
            options.update({
                'interactive': False,
                'inhibit_post_migrate': True
            })

        return super(Command, self).handle(**options)

    @staticmethod
    def emit_post_syncdb(verbosity, interactive, database):
        engine = get_engine_from_db_alias(database)
        if engine != 'django_cassandra_engine':
            return FlushCommand.emit_post_syncdb(verbosity, interactive,
                                                 database)

    @staticmethod
    def emit_post_migrate(verbosity, interactive, database):
        engine = get_engine_from_db_alias(database)
        if engine != 'django_cassandra_engine':
            return FlushCommand.emit_post_migrate(verbosity, interactive,
                                                  database)
