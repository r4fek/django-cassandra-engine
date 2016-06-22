from django_cassandra_engine.serializers import DjangoCassandraModelSerializer

from common.models import CassandraThingWithDate


class ThingSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = CassandraThingWithDate
        fields = '__all__'
