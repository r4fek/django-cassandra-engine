from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response

from .models import CassandraThingMultiplePK, CassandraThing
from .serializers import ThingSerializer, ThingMultiplePKSerializer


class ThingMultiplePKViewSet(ViewSet):
    def list(self, request):
        queryset = CassandraThingMultiplePK.objects.all()
        serializer =ThingMultiplePKSerializer(queryset, many=True)
        return Response(serializer.data)


class ThingMultiplePKListCreateAPIView(ListCreateAPIView):
    queryset = CassandraThingMultiplePK.objects.all()
    serializer_class = ThingMultiplePKSerializer
    permission_classes = ()


class ThingMultiplePKListAPIView(ListAPIView):
    queryset = CassandraThingMultiplePK.objects.all()
    serializer_class = ThingMultiplePKSerializer
    permission_classes = ()


class CassandraThing2ViewSet(ModelViewSet):
    serializer_class = ThingSerializer
    queryset = CassandraThing.objects.all()
    permission_classes = ()
