from cassandra.cqlengine import columns, models


class TestModel(models.Model):
    __connection__ = "cassandra"
    __keyspace__ = "db"

    id = columns.BigInt(primary_key=True)
    created_at = columns.DateTime()
    deleted = columns.Boolean(default=False)


class TestModel2(models.Model):
    __connection__ = "cassandra2"
    __keyspace__ = "db2"

    id = columns.BigInt(primary_key=True)


class TestModel3(models.Model):
    __connection__ = "cassandra2"
    __keyspace__ = "db2"

    id = columns.BigInt(primary_key=True)
