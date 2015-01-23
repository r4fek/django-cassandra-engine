from cqlengine import columns, Model


class ExampleModel(Model):
    id = columns.BigInt(primary_key=True)
    created_at = columns.DateTime()
    deleted = columns.Boolean(default=False)


class ExampleModel2(Model):
    id = columns.BigInt(primary_key=True)


class TestProjectModel(Model):
    id = columns.UUID(primary_key=True)
