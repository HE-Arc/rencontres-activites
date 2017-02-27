from django.conf.urls import url, include

from .views import ActivityFormViewCreate, ActivityFormViewUpdate, index
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^activity/$', views.index),
    url(r'activity/create/$', ActivityFormViewCreate.as_view(), name='activity-add'),
    url(r'activity/update/(?P<pk>[0-9]+)/$', ActivityFormViewUpdate.as_view(), name='activity-update')

]