import os

from django.apps import AppConfig as DjangoAppConfig

from .compat import columns


class CallableBool:
    """
    An boolean-like object that is also callable for backwards compatibility.
    """

    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return self.value

    def __call__(self):
        return self.value

    def __nonzero__(self):  # Python 2 compatibility
        return self.value

    def __repr__(self):
        return 'CallableBool(%r)' % self.value

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __or__(self, other):
        return bool(self.value or other)

    def __hash__(self):
        return hash(self.value)


def has_default(self):
    return CallableBool(self.default is not None)


# monkey patch Column.has_default to be able to use function call too
columns.Column.has_default = property(has_default)

if os.getenv('CQLENG_ALLOW_SCHEMA_MANAGEMENT') is None:
    os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'


class AppConfig(DjangoAppConfig):
    name = 'django_cassandra_engine'

    def connect(self):
        from django_cassandra_engine.utils import get_cassandra_connections

        for _, conn in get_cassandra_connections():
            conn.connect()

    def import_models(self, *args, **kwargs):
        self.connect()
        return super().import_models(*args, **kwargs)
