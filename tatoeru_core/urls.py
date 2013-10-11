from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^error$', views.error, name='error'),
    url(r'^motomeru$', views.motomeru, name='motomeru'),
    url(r'^send_motomeru_request$',
        views.send_motomeru_request,
        name='send_motomeru_request'),
    url(r'^kotaeru/(?P<post_id>\d+)$', views.kotaeru, name='kotaeru'),
    url(r'^send_kotaeru_request$',
        views.send_kotaeru_request,
        name='send_kotaeru_request'),
)
