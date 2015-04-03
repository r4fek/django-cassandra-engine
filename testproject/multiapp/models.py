from cassandra.cqlengine import columns
from cassandra.cqlengine import models


class TestModel(models.Model):
    __keyspace__ = 'db'

    id = columns.BigInt(primary_key=True)
    created_at = columns.DateTime()
    deleted = columns.Boolean(default=False)


class TestModel2(models.Model):
    __keyspace__ = 'db2'
    id = columns.BigInt(primary_key=True)


class TestModel3(models.Model):
    __keyspace__ = 'db2'
    id = columns.BigInt(primary_key=True)
