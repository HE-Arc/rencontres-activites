from django.conf.urls import url, include

from .views import ActivityFormViewCreate, ActivityFormViewUpdate, dashboard
from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/',include('registration.backends.simple.urls'), name='registration_register'),
    url(r'^login', auth_views.login, name='login'),
    url(r'^logout', auth_views.logout, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^matchmaking/$', views.matchmaking, name="matchmaking"),
    url(r'^matchmaking/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)$', views.matchmaking, name="matchmaking"),
    url(r'activity/create/$', ActivityFormViewCreate.as_view(), name='activity-add'),
    url(r'activity/update/(?P<pk>[0-9]+)/$', ActivityFormViewUpdate.as_view(), name='activity-update'),
    url(r'^activity/(?P<pk>[0-9]+)/$', views.ActivityDetailView.as_view(), name='activity'),
]
