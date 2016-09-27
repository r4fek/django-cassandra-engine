import uuid

from cassandra.cqlengine import columns as cassandra_columns

from django_cassandra_engine.models import DjangoCassandraModel


class CassandraThing(DjangoCassandraModel):
    id = cassandra_columns.UUID(primary_key=True, default=uuid.uuid4)
    data_abstract = cassandra_columns.Text(max_length=10)
