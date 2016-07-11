from django_cassandra_engine.serializers import DjangoCassandraModelSerializer

from common.models import CassandraThingMultiplePK, CassandraThing


class ThingMultiplePKSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = CassandraThingMultiplePK
        fields = '__all__'


class ThingSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = CassandraThing
        fields = '__all__'
