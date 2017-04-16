from django.conf.urls import url, include

from .views import ActivityFormViewCreate, ActivityFormViewUpdate, dashboard, UserProfileDetailView
from . import views
from app.views import *

from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^accounts/',include('registration.backends.simple.urls'), name='registration_register'),
    url(r'^login', auth_views.login, name='login'),
    url(r'^logout', auth_views.logout, name='logout'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^matchmaking/$', matchmaking, name="matchmaking"),
    url(r'^matchmaking/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)$', matchmaking, name="matchmaking"),
    url(r'activity/create/$', ActivityFormViewCreate.as_view(), name='activity-add'),
    url(r'activity/update/(?P<pk>[0-9]+)/$', ActivityFormViewUpdate.as_view(), name='activity-update'),
    url(r'^activity/(?P<pk>[0-9]+)/$', ActivityDetailView.as_view(), name='activity'),
    url(r'^profile/?(?P<pk>[0-9]+)/$', UserProfileDetailView.as_view(), name='profile'),
    url(r'profile/update/$', views.update_profile, name='profile-update'),
    url(r'friend/add', views.AddUserAsAFriend.as_view(), name='add-friend'),
    url(r'friend/manage', views.ManageFriendshipRequest.as_view(), name='manage-friend'),
    url(r'friend/remove', views.RemoveFriend.as_view(), name='remove-friend')
]
