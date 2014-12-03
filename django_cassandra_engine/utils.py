import inspect
import cqlengine
import django


class CursorWrapper(object):
    """
    Simple CursorWrapper implementation based on django.db.utils.CursorWrapper
    """

    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    WRAP_ERROR_ATTRS = frozenset(['fetchone', 'fetchmany', 'fetchall',
                                  'nextset'])

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
        return apps.get_apps()
    else:
        from django.db import models
        return models.get_apps()


def get_cql_models(app):
    """
    :param app: django models module
    :return: list of all cqlengine.Model within app
    """

    models = []
    for name, obj in inspect.getmembers(app):
        if inspect.isclass(obj) and issubclass(obj, cqlengine.Model) \
                and not obj.__abstract__:
            models.append(obj)

    return models


def get_cassandra_connection():
    from django.db import connections
    for alias in connections:
        engine = connections[alias].settings_dict.get('ENGINE', '')
        if engine == 'django_cassandra_engine':
            return connections[alias]
