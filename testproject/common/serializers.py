from rest_framework import serializers

from common.models import (
    CassandraFamilyMember,
    CassandraThing,
    CassandraThingMultiplePK,
)
from django_cassandra_engine.rest.serializers import (
    DjangoCassandraModelSerializer,
)


class ThingMultiplePKSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = CassandraThingMultiplePK
        fields = "__all__"


class ThingSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = CassandraThing
        fields = "__all__"


class CassandraFamilyMemberSerializer(DjangoCassandraModelSerializer):
    is_real = serializers.BooleanField()

    class Meta:
        model = CassandraFamilyMember
        fields = "__all__"
