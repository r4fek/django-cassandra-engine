from cassandra import ConsistencyLevel
from cqlengine import connection
from djangotoolbox.db.base import FakeCursor


class CassandraConnection(object):

    def __init__(self, **options):

        self.hosts = options.pop('HOST')
        self.keyspace = options.pop('NAME')
        self.options = options.pop('OPTIONS')
        self.setup()

    def setup(self):

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

    @property
    def cluster(self):
        return connection.get_cluster()

    def close(self):
        self.cluster.shutdown()