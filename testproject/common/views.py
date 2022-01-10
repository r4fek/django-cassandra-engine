from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import CassandraThing, CassandraThingMultiplePK
from .serializers import ThingMultiplePKSerializer, ThingSerializer


class ThingMultiplePKViewSet(ViewSet):
    def list(self, request):
        queryset = CassandraThingMultiplePK.objects.all()
        serializer = ThingMultiplePKSerializer(queryset, many=True)
        return Response(serializer.data)


class ThingMultiplePKListCreateAPIView(ListCreateAPIView):
    queryset = CassandraThingMultiplePK.objects.all()
    serializer_class = ThingMultiplePKSerializer
    permission_classes = ()


class ThingMultiplePKListAPIView(ListAPIView):
    queryset = CassandraThingMultiplePK.objects.all()
    serializer_class = ThingMultiplePKSerializer
    permission_classes = ()


class ThingModelViewSet(ModelViewSet):
    serializer_class = ThingSerializer
    queryset = CassandraThing.objects.all()
    permission_classes = ()
