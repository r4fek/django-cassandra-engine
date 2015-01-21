from cqlengine import columns, Model


class TestModel(Model):
    __keyspace__ = 'db'

    id = columns.BigInt(primary_key=True)
    created_at = columns.DateTime()
    deleted = columns.Boolean(default=False)


class TestModel2(Model):
    __keyspace__ = 'db2'
    id = columns.BigInt(primary_key=True)


class TestModel3(Model):
    id = columns.BigInt(primary_key=True)
