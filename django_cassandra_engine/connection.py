from django_cassandra_engine.utils import get_cassandra_connections
from .compat import (
    CQLEngineException,
    PlainTextAuthProvider,
    Session,
    connection,
    Cluster
)

class Cursor(object):
    def __init__(self, connection):
        self.connection = connection

    def execute(self, *args, **kwargs):
        return self.connection.execute(*args, **kwargs)

    def close(self):
        pass

    def fetchmany(self, _):
        return []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()


class FakeConnection(object):
    def commit(self):
        pass

    def rollback(self):
        pass

    def cursor(self):
        return Cursor(None)

    def close(self):
        pass


class CassandraConnection(object):
    def __init__(self, alias, **options):
        self.alias = alias
        self.hosts = options.get('HOST').split(',')
        self.keyspace = options.get('NAME')
        self.user = options.get('USER')
        self.password = options.get('PASSWORD')
        self.options = options.get('OPTIONS', {})
        self.cluster_options = self.options.get('connection', {})
        self.session_options = self.options.get('session', {})
        self.connection_options = {
            'lazy_connect': self.cluster_options.pop('lazy_connect', False),
            'retry_connect': self.cluster_options.pop('retry_connect', False),
            'consistency': self.cluster_options.pop('consistency', None),
        }
        if (
            self.user
            and self.password
            and 'auth_provider' not in self.cluster_options
        ):
            self.cluster_options['auth_provider'] = PlainTextAuthProvider(
                username=self.user, password=self.password
            )

        self.default = (
            alias == 'default'
            or len(list(get_cassandra_connections())) == 1
            or self.cluster_options.pop('default', False)
        )

        self.register()

    def register(self):
        try:
            connection.get_connection(name=self.alias)
        except CQLEngineException:
            if self.default:
                from cassandra.cqlengine import models

                models.DEFAULT_KEYSPACE = self.keyspace

            for option, value in self.session_options.items():
                setattr(Session, option, value)
            if 'cloud' in self.cluster_options:
                cluster = Cluster(**self.cluster_options)
                session = cluster.connect()
                connection.register_connection(
                    self.alias,
                    default=self.default,
                    session=session
                )
            else:
                connection.register_connection(
                    self.alias,
                    hosts=self.hosts,
                    default=self.default,
                    cluster_options=self.cluster_options,
                    **self.connection_options
                )   

    @property
    def cluster(self):
        return connection.get_cluster(connection=self.alias)

    @property
    def session(self):
        return connection.get_session(connection=self.alias)

    def commit(self):
        pass

    def rollback(self):
        pass

    def cursor(self):
        return Cursor(self)

    def execute(self, qs, *args, **kwargs):
        self.session.set_keyspace(self.keyspace)
        return self.session.execute(qs, *args, **kwargs)

    def close(self):
        """ We would like to keep connection always open by default """

    def unregister(self):
        """
        Unregister this connection
        """
        connection.unregister_connection(self.alias)
