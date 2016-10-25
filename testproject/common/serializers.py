from common.models import (
    CassandraThingMultiplePK, CassandraThing, CassandraFamilyMember
)
from rest_framework import serializers

from django_cassandra_engine.rest.serializers import DjangoCassandraModelSerializer


class ThingMultiplePKSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = CassandraThingMultiplePK
        fields = '__all__'


class ThingSerializer(DjangoCassandraModelSerializer):

    class Meta:
        model = CassandraThing
        fields = '__all__'


class CassandraFamilyMemberSerializer(DjangoCassandraModelSerializer):
    is_real = serializers.NullBooleanField()

    class Meta:
        model = CassandraFamilyMember
        fields = '__all__'
