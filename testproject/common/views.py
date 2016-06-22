from rest_framework import viewsets
from rest_framework.response import Response

from .models import CassandraThingWithDate
from .serializers import ThingSerializer


# class ThingList(ListAPIView):
#     queryset = CassandraThingWithDate.objects.all()
#     serializer_class = ThingSerializer


class ThingList(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = CassandraThingWithDate.objects.all()
        serializer = ThingSerializer(queryset, many=True)
        return Response(serializer.data)
