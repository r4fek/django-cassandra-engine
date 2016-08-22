from django.core.management.commands.makemigrations import (
    Command as MakeMigrationsCommand
)
from django.db import connections
from django_cassandra_engine.utils import get_cassandra_connections


class Command(MakeMigrationsCommand):

    @staticmethod
    def _change_cassandra_engine_name(name):
        for alias, _ in get_cassandra_connections():
            connections[alias].settings_dict['ENGINE'] = name

    def handle(self, *args, **options):
        """
        Pretend django_cassandra_engine to be dummy database backend
        with no support for migrations.
        """
        self._change_cassandra_engine_name('django.db.backends.dummy')
        try:
            super(Command, self).handle(*args, **options)
        finally:
            self._change_cassandra_engine_name('django_cassandra_engine')
