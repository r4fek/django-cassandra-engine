from cqlengine import columns, Model


class ExampleModel(Model):
    __keyspace__ = 'db'
    id = columns.BigInt(primary_key=True)
    created_at = columns.DateTime()
    deleted = columns.Boolean(default=False)


class ExampleModel2(Model):
    __keyspace__ = 'db'
    id = columns.BigInt(primary_key=True)


class TestProjectModel(Model):
    __keyspace__ = 'db'
    id = columns.UUID(primary_key=True)
