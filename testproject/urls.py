from django.urls import include, re_path

from testproject.app import views

urlpatterns = [
    re_path(r"^$", views.home, name="home"),
    re_path(r"^common/", include("common.urls")),
]
