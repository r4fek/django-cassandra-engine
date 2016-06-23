from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response

from .models import CassandraThingMultiplePK
from .serializers import ThingSerializer


class ThingViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = CassandraThingMultiplePK.objects.all()
        serializer = ThingSerializer(queryset, many=True)
        return Response(serializer.data)


class ThingListCreateAPIView(ListCreateAPIView):
    queryset = CassandraThingMultiplePK.objects.all()
    serializer_class = ThingSerializer
    permission_classes = ()


class ThingListAPIView(ListAPIView):
    queryset = CassandraThingMultiplePK.objects.all()
    serializer_class = ThingSerializer
    permission_classes = ()
