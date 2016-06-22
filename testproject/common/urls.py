from django.conf.urls import url

from .views import ThingList

urlpatterns = [
    url(r'^things/$', ThingList.as_view({'get': 'list'}), name='thing_api'),
]
