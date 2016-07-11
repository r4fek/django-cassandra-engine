from django.conf.urls import include, url
from rest_framework import routers

from .views import ThingMultiplePKViewSet, ThingMultiplePKListCreateAPIView, ThingMultiplePKListAPIView, ThingModelViewSet

router = routers.DefaultRouter()
router.register(r'thing-modelviewset', ThingModelViewSet)

urlpatterns = [
    url(r'^thing-viewset/$', ThingMultiplePKViewSet.as_view({'get': 'list'}), name='thing_viewset_api'),
    url(r'^thing-listcreate/$', ThingMultiplePKListCreateAPIView.as_view(), name='thing_listcreate_api'),
    url(r'^thing-listview/$', ThingMultiplePKListAPIView.as_view(), name='thing_listview_api'),
    url(r'^', include(router.urls)),
]
