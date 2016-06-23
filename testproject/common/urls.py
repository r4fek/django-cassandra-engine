from django.conf.urls import url

from .views import ThingViewSet, ThingListCreateAPIView, ThingListAPIView

urlpatterns = [
    url(r'^thing-viewset/$', ThingViewSet.as_view({'get': 'list'}), name='thing_viewset_api'),
    url(r'^thing-listcreate/$', ThingListCreateAPIView.as_view(), name='thing_listcreate_api'),
    url(r'^thing-listview/$', ThingListAPIView.as_view(), name='thing_listview_api'),
]
