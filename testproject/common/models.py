import uuid

from cassandra.cqlengine import columns as cassandra_columns

from django_cassandra_engine.models import DjangoCassandraModel


class CassandraThingMultiplePK(DjangoCassandraModel):
    __keyspace__ = "db"
    id = cassandra_columns.UUID(primary_key=True, default=uuid.uuid4)
    another_id = cassandra_columns.UUID(primary_key=True, default=uuid.uuid4)
    data_abstract = cassandra_columns.Text(max_length=10)
    created_on = cassandra_columns.DateTime()

    class Meta:
        get_pk_field = "id"


class CassandraThing(DjangoCassandraModel):
    __keyspace__ = "db"
    id = cassandra_columns.UUID(primary_key=True, default=uuid.uuid4)
    data_abstract = cassandra_columns.Text(max_length=10)

    class Meta:
        get_pk_field = "id"


class CassandraFamilyMember(DjangoCassandraModel):
    __keyspace__ = "db"
    id = cassandra_columns.UUID(primary_key=True, default=uuid.uuid4)
    first_name = cassandra_columns.Text(primary_key=True)
    last_name = cassandra_columns.Text(primary_key=True)
    is_real = cassandra_columns.Boolean(default=False)
    favourite_number = cassandra_columns.Integer(required=False)
    favourite_float_number = cassandra_columns.Float(partition_key=True)
    created_on = cassandra_columns.DateTime()

    class Meta:
        get_pk_field = "id"
