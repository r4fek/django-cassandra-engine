from cassandra import ConsistencyLevel
from cqlengine import connection
from djangotoolbox.db.base import FakeCursor


class CassandraConnection(object):

    def __init__(self, **options):

        self.hosts = options.get('HOST').split(',')
        self.keyspace = options.get('NAME')
        self.options = options.get('OPTIONS', {})
        self.setup()

    def setup(self):
        if connection.cluster is not None:
            # already connected
            return

        connection.setup(
            self.hosts,
            self.keyspace,
            consistency=self.options.get('consistency_level',
                                         ConsistencyLevel.ONE)
        )

    def commit(self):
        pass

    def rollback(self):
        pass

    def cursor(self):
        return FakeCursor()

    @property
    def session(self):
        return connection.get_session()

    def execute(self, qs):
        self.session.set_keyspace(self.keyspace)
        self.session.execute(qs)

    @property
    def cluster(self):
        return connection.get_cluster()

    def close(self):
        """ We would like to keep connection always open by default """

    def close_all(self):
        """
        Close all db connections
        """

        self.cluster.shutdown()
        connection.cluster = None
        connection.session = None
        connection.lazy_connect_args = None
        connection.default_consistency_level = None
