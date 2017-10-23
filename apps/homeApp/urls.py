from django.conf.urls import url, include
from . import views
# from views import AutoCompleteView

urlpatterns = [
    url(r'^$', views.index),
    url(r'^api/get_places', views.get_places, name='get_places'),
    url(r'^search/users', views.searchUsers),
    url(r'^search/$', views.search),
    # url(r'^autocomplete/$', AutoCompleteView.as_view(), name='autocomplete'),

]
