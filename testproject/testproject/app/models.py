from cqlengine import columns, Model


class ExampleModel(Model):
    id = columns.BigInt(primary_key=True)
    created_at = columns.DateTime()
    deleted = columns.Boolean(default=False)
