from django.conf.urls import url
from . import views

urlpatterns = [
    #GET
    url(r'^login$', views.login_page),
    url(r'^register$', views.register_page),
    url(r'^profile$', views.profile),
    url(r'^user/(?P<id>\d+)$', views.user_page),
    url(r'^searchusers$', views.searchUserDB),

    #POSTS
    url(r'^register_account$', views.register_account),
    url(r'^log_user_in$', views.log_user_in),
    url(r'^createProfile$', views.createProfile),
    url(r'^editProfile$', views.editProfile),
    url(r'^logout$', views.logout),
    url(r'^connect/(?P<operation>.+)/(?P<id>\d+)/$', views.change_friends),
    url(r'^newProfilePicture$', views.newProfilePicture),
    url(r'^editProfilePicture$', views.editProfilePicture),


]
