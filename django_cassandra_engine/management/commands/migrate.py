from django.core.management import call_command
from django.core.management.commands.migrate import Command as MigrateCommand

from django_cassandra_engine.utils import get_engine_from_db_alias


class Command(MigrateCommand):

    def handle(self, *args, **options):
        engine = get_engine_from_db_alias(options['database'])

        # Call regular migrate if engine is different from ours
        if engine != 'django_cassandra_engine':
            return super(Command, self).handle(*args, **options)
        else:
            self.stdout.write("Migrations are not supported in this engine. "
                              "Calling syncdb instead..")
            call_command('syncdb', **options)
