from django.conf.urls import url, include
from . import views


urlpatterns = [

    # get routes ===============
    url(r'^movie/(?P<id>\d+)$', views.movie_page),
    url(r'^people/(?P<id>\d+)', views.cast_page),
    url(r'^show/(?P<id>\d+)', views.show_page),
    url(r'^episode/(?P<id>\d+)/(?P<season>\d+)/(?P<episode>\d+)$', views.show_episode),
    url(r'^seasonData/$', views.seasonData),
    url(r'^discover$', views.discover),
    url(r'^discover/(?P<id>\d+)$', views.discover_more),
    url(r'^add/watchlist/$', views.add_to_watchlist),

    # postroutes ===============
    url(r'^makeReview/(?P<id>\d+)/(?P<season>\d+)/(?P<episode>\d+)$', views.makeReview),
    url(r'^movie/delete/watchlist/(?P<id>\d+)$', views.delete_from_watchlist),
]
