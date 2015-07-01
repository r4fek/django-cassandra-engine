from cassandra.cluster import Session
from cassandra.cqlengine import connection
from cassandra.auth import PlainTextAuthProvider


class Cursor(object):
    def __init__(self, connection):
        self.connection = connection

    def execute(self, *args, **kwargs):
        return self.connection.execute(*args, **kwargs)

    def close(self):
        pass

    def fetchmany(self, _):
        return []


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

    def __init__(self, **options):

        self.hosts = options.get('HOST').split(',')
        self.keyspace = options.get('NAME')
        self.user = options.get('USER')
        self.password = options.get('PASSWORD')
        self.options = options.get('OPTIONS', {})
        self.connection_options = self.options.get('connection', {})
        self.session_options = self.options.get('session', {})

        if self.user and self.password and \
                'auth_provider' not in self.connection_options:
            self.connection_options['auth_provider'] = \
                PlainTextAuthProvider(username=self.user,
                                      password=self.password)

        self.setup()

    def setup(self):
        from cassandra.cqlengine import connection
        if connection.cluster is not None:
            # already connected
            return
        connection.setup(self.hosts, self.keyspace, **self.connection_options)

        consistency = self.connection_options.get('consistency')
        if consistency:
            self.session.default_consistency_level = consistency
        for option, value in self.session_options.items():
            setattr(Session, option, value)

    def commit(self):
        pass

    def rollback(self):
        pass

    def cursor(self):
        return Cursor(self)

    @property
    def session(self):
        return connection.get_session()

    @property
    def cluster(self):
        return connection.get_cluster()

    def execute(self, qs, *args, **kwargs):
        self.session.set_keyspace(self.keyspace)
        return self.session.execute(qs, *args, **kwargs)

    def close(self):
        """ We would like to keep connection always open by default """

    def close_all(self):
        """
        Close all db connections
        """

        if self.cluster is not None:
            self.cluster.shutdown()
        if self.session is not None:
            self.session.shutdown()

        connection.cluster = None
        connection.session = None
        connection.lazy_connect_args = None
        connection.default_consistency_level = None
