from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^openid/', include('django_openid_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',
        include('tatoeru_core.urls', namespace='tatoeru_core')),
)
