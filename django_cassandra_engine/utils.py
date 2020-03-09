import inspect

import django
from django.conf import settings
from django.db import DEFAULT_DB_ALIAS

from .compat import cqlengine


class CursorWrapper(object):
    """
    Simple CursorWrapper implementation based on django.db.utils.CursorWrapper
    """

    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    WRAP_ERROR_ATTRS = frozenset(
        ['fetchone', 'fetchmany', 'fetchall', 'nextset']
    )

    def __getattr__(self, attr):
        cursor_attr = getattr(self.cursor, attr)
        if attr in CursorWrapper.WRAP_ERROR_ATTRS:
            return self.db.wrap_database_errors(cursor_attr)
        else:
            return cursor_attr

    def __iter__(self):
        return iter(self.cursor)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def callproc(self, procname, params=None):
        with self.db.wrap_database_errors:
            if params is None:
                return self.cursor.callproc(procname)
            else:
                return self.cursor.callproc(procname, params)

    def execute(self, sql, params=None):
        with self.db.wrap_database_errors:
            if params is None:
                return self.cursor.execute(sql)
            else:
                return self.cursor.execute(sql, params)

    def executemany(self, sql, param_list):
        with self.db.wrap_database_errors:
            return self.cursor.executemany(sql, param_list)


def get_installed_apps():
    """
    Return list of all installed apps
    """
    if django.VERSION >= (1, 7):
        from django.apps import apps

        return [
            a.models_module
            for a in apps.get_app_configs()
            if a.models_module is not None
        ]
    else:
        from django.db import models

        return models.get_apps()


def get_cql_models(app, connection=None, keyspace=None):
    """
    :param app: django models module
    :param connection: connection name
    :param keyspace: keyspace
    :return: list of all cassandra.cqlengine.Model within app that should be
    synced to keyspace.
    """
    from .models import DjangoCassandraModel

    models = []
    single_cassandra_connection = len(list(get_cassandra_connections())) == 1
    is_default_connection = (
        connection == DEFAULT_DB_ALIAS or single_cassandra_connection
    )

    for name, obj in inspect.getmembers(app):
        cql_model_types = (cqlengine.models.Model, DjangoCassandraModel)
        if (
            inspect.isclass(obj)
            and issubclass(obj, cql_model_types)
            and not obj.__abstract__
        ):
            if (
                obj.__connection__ == connection
                or (obj.__connection__ is None and is_default_connection)
                or obj.__connection__ is None
                and obj.__keyspace__ is not None
                and obj.__keyspace__ == keyspace
            ):
                models.append(obj)

    return models


def get_cassandra_connections():
    """
    :return: List of tuples (db_alias, connection) for all cassandra
    connections in DATABASES dict.
    """

    from django.db import connections

    for alias in connections:
        engine = connections[alias].settings_dict.get('ENGINE', '')
        if engine == 'django_cassandra_engine':
            yield alias, connections[alias]


def get_default_cassandra_connection():
    """
    Return first default cassandra connection
    :return:
    """
    for alias, conn in get_cassandra_connections():
        if conn.connection.default:
            return alias, conn

    return list(get_cassandra_connections())[0]


def get_cassandra_connection(alias=None, name=None):
    """
    :return: cassandra connection matching alias or name or just first found.
    """

    for _alias, connection in get_cassandra_connections():
        if alias is not None:
            if alias == _alias:
                return connection
        elif name is not None:
            if name == connection.settings_dict['NAME']:
                return connection
        else:
            return connection


def get_cassandra_db_aliases():
    from django.db import connections

    for alias in connections:
        engine = connections[alias].settings_dict.get('ENGINE', '')
        if engine == 'django_cassandra_engine':
            yield alias


def get_cassandra_db_alias():
    return get_cassandra_db_aliases().__next__()


def get_engine_from_db_alias(db_alias):
    """
    :param db_alias: database alias
    :return: database engine from DATABASES dict corresponding to db_alias
             or None if db_alias was not found
    """

    return settings.DATABASES.get(db_alias, {}).get('ENGINE', None)
