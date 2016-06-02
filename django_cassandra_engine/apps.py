from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'django_cassandra_engine'

    def ready(self):
        from django_cassandra_engine.utils import get_cassandra_connections
        for _, conn in get_cassandra_connections():
            conn.connect()
