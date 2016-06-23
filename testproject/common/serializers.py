from django_cassandra_engine.serializers import DjangoCassandraModelSerializer

from common.models import CassandraThingMultiplePK


class ThingSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = CassandraThingMultiplePK
        fields = '__all__'
