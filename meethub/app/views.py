from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views import View, generic

from .models import Activity as ActivityModel
from .models import Activity

from .forms import ActivityForm


def index(request):
    return render(request, 'pages/index.html')


def dashboard(request):
    # if request.user.is_authenticated :
    #    render(request, 'pages/index.html')
    context = {}
    # Get the informations of the logged user

    # Get the three latest activities done by the user

    # Get the three next activities of the user

    # Get all the activities that are opened next to the user


    activities = Activity.objects.all()
    context['activities'] = activities
    return render(request, 'pages/dashboard.html', context)


@login_required
def matchmaking(request, lat=None, long=None):
    """
    Get events near user if lat and long not none, otherwise request location
    :param request:
    :return:
    """
    if lat and long:
        activities = Activity.get_activities_near(lat, long)
        return render(request, 'pages/matchmaking/index.html', {"activities": activities})
    else:
        return render(request, 'pages/matchmaking/ask_location.html', {})


class ActivityFormViewCreate(CreateView):
    template_name = 'activity/create.html'
    form_class = ActivityForm
    success_url = '/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['users'].queryset = Activity.get_waiting_users(self.request.user)
        return form

    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super(ActivityFormViewCreate, self).form_valid(form)


class ActivityFormViewUpdate(UpdateView):
    template_name = 'activity/create.html'
    form_class = ActivityForm
    success_url = '/'
    model = ActivityModel


class ActivityDetailView(generic.DetailView):
    model = Activity
    template_name = 'activity/index.html'
    context_object_name = 'activity'
