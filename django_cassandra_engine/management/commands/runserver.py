from django.core.management.commands.runserver import Command as RunserverCmd
from django.conf import settings
from django.db import DEFAULT_DB_ALIAS


class Command(RunserverCmd):

    def check_migrations(self):
        """
        Skip checking migrations if engine == django_cassandra_engine.
        """

        engine = settings.DATABASES[DEFAULT_DB_ALIAS].get('ENGINE', '')
        if engine != 'django_cassandra_engine':
            return super(Command, self).check_migrations()
