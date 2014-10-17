from django.conf import settings
from django.core.management import call_command
from django.core.management.commands.migrate import Command as MigrateCommand


class Command(MigrateCommand):

    def handle(self, *args, **options):
        db = options.get('database')
        engine = settings.DATABASES.get(db, {}).get('ENGINE', '')

        # Call regular migrate if engine is different from ours
        if engine != 'django_cassandra_engine':
            return super(Command, self).handle(**options)
        else:
            self.stdout.write("Migrations are not supported in this engine. "
                              "Calling syncdb instead..")
            call_command('syncdb', **options)
