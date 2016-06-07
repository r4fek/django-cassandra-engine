from django.apps import AppConfig

from django_cassandra_engine.utils import get_cassandra_connections


class AppConfig(AppConfig):
    name = 'django_cassandra_engine'

    def ready(self):
        for _, conn in get_cassandra_connections():
            conn.connect()
