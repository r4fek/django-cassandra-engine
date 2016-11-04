from cassandra.cqlengine import columns
from cassandra.cqlengine import models
from cassandra.cqlengine.columns import UserDefinedType
from cassandra.cqlengine.usertype import UserType


class ExampleModel(models.Model):
    id = columns.BigInt(primary_key=True)
    created_at = columns.DateTime()
    deleted = columns.Boolean(default=False)


class ExampleModel2(models.Model):
    id = columns.BigInt(primary_key=True)


class TestProjectModel(models.Model):
    id = columns.UUID(primary_key=True)


class SimpleUDT(UserType):
    name = columns.Text()
    value = columns.Integer()


class ExampleModelWithUDT(models.Model):
    id = columns.UUID(primary_key=True)
    sth = UserDefinedType(SimpleUDT)
