from django.urls import include, re_path
from rest_framework import routers

from .views import (
    ThingModelViewSet,
    ThingMultiplePKListAPIView,
    ThingMultiplePKListCreateAPIView,
    ThingMultiplePKViewSet,
)

router = routers.DefaultRouter()
router.register(r"thing-modelviewset", ThingModelViewSet)

urlpatterns = [
    re_path(
        r"^thing-viewset/$",
        ThingMultiplePKViewSet.as_view({"get": "list"}),
        name="thing_viewset_api",
    ),
    re_path(
        r"^thing-listcreate/$",
        ThingMultiplePKListCreateAPIView.as_view(),
        name="thing_listcreate_api",
    ),
    re_path(
        r"^thing-listview/$",
        ThingMultiplePKListAPIView.as_view(),
        name="thing_listview_api",
    ),
    re_path(r"^", include(router.urls)),
]
