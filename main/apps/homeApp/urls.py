from django.conf.urls import url, include
from . import views
# from views import AutoCompleteView

urlpatterns = [
    url(r'^$', views.index),
    url(r'^testing$', views.testing),
    url(r'^api/get_places', views.get_places, name='get_places'),
    url(r'^search/users', views.searchUsers),
    url(r'^reviewfeed', views.feed),
    url(r'^api/search_movies', views.search_movies, name='search_movies'),
    url(r'^search/$', views.search),
    # url(r'^autocomplete/$', AutoCompleteView.as_view(), name='autocomplete'),

]
