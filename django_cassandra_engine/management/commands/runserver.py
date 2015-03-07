from django.core.management import get_commands
from django.db import DEFAULT_DB_ALIAS

from django_cassandra_engine.utils import get_engine_from_db_alias


RunserverCmd = get_commands()['runserver']


class Command(RunserverCmd):

    def check_migrations(self):
        """
        Skip checking migrations if engine == django_cassandra_engine.
        """

        engine = get_engine_from_db_alias(DEFAULT_DB_ALIAS)
        if engine != 'django_cassandra_engine':
            return super(Command, self).check_migrations()
