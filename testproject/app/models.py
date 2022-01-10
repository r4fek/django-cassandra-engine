from cassandra.cqlengine import columns, models


class ExampleModel(models.Model):
    id = columns.BigInt(primary_key=True)
    created_at = columns.DateTime()
    deleted = columns.Boolean(default=False)


class ExampleModel2(models.Model):
    id = columns.BigInt(primary_key=True)


class TestProjectModel(models.Model):
    id = columns.UUID(primary_key=True)
