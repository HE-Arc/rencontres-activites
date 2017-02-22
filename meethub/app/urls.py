from django.conf.urls import url

from .views import Activity
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^activity/$', Activity.as_view())

]