from django.conf.urls import url, include
from . import views


urlpatterns = [

    # get routes ===============
    url(r'^movie/(?P<id>\d+)$', views.movie_page),
    url(r'^people/(?P<id>\d+)', views.cast_page),
    url(r'^show/(?P<id>\d+)', views.show_page),
    url(r'^movie_home$', views.movie_home),
    url(r'^tv_home$', views.tv_home),
    url(r'^actor_home$', views.actor_home),
    url(r'^season/(?P<id>\d+)/(?P<season>\d+)/$', views.show_season),
    url(r'^episode/(?P<id>\d+)/(?P<season>\d+)/(?P<episode>\d+)$', views.show_episode),

    # postroutes ===============
    url(r'^movie/add/watchlist/(?P<id>\d+)$', views.add_to_watchlist),
    url(r'^makeReview/(?P<id>\d+)/(?P<season>\d+)/(?P<episode>\d+)$', views.makeReview),
    url(r'^movie/delete/watchlist/(?P<id>\d+)$', views.delete_from_watchlist),
]
