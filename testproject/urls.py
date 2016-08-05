from django.conf.urls import include, url

from django.contrib import admin

from testproject.app import views


urlpatterns = [
    # Examples:
    url(r'^$', views.home, name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
