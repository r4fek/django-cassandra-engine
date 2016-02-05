from threading import Lock

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

        self.lock = Lock()
        self.session = None
        self.cluster = None
        self.setup()

    def setup(self):
        with self.lock:
            self.session = connection.get_session()
            if not (self.session is None or self.session.is_shutdown):
                # already connected
                return

            for option, value in self.session_options.items():
                setattr(Session, option, value)
            connection.setup(self.hosts, self.keyspace,
                             **self.connection_options)
            self.session = connection.get_session()
            self.cluster = connection.get_cluster()

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

    def close_all(self):
        """
        Close all db connections
        """
        with self.lock:
            if self.cluster is not None:
                self.cluster.shutdown()

            if self.session is not None and not self.session.is_shutdown:
                self.session.shutdown()

            self.session = None
            self.cluster = None
