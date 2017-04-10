import base64
import calendar
import hmac
import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.views.generic import CreateView
from django.views.generic import UpdateView
from pygeocoder import Geocoder

from .forms import ActivityForm
from .models import Activity, get_activities_near, get_waiting_users
from .models import Activity as ActivityModel
from secret import *


def index(request):
    return render(request, 'pages/index.html')


@login_required
def dashboard(request):
    today = datetime.now()
    u = request.user

    context = {}
    # Get the informations of the logged user

    # Get the three latest activities done by the user
    activities_done_by_the_user = u.participants.filter(date__lte=today).order_by('-date')[:3];
    # Get the three next activities of the user
    next_activities_of_the_user = u.participants.filter(date__gte=today).order_by('date')[:3]
    # Get the first 10 upcoming activities.
    upcoming_activities = Activity.objects.filter(date__gte=today).order_by('date')[:10]

    # Give the informations to the view
    context['activities_done'] = activities_done_by_the_user
    context['next_activities'] = next_activities_of_the_user
    context['upcoming_activities'] = upcoming_activities

    context['api_key_map'] = "AIzaSyD48NmCV_kXSHmaGQSdEGojD7vkcRcNqME"

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
        # TODO: check where there's still place && add user to waiting list
        activities = get_activities_near(lat, long).filter(date__gte=datetime.now().date())
        return render(request, 'pages/matchmaking/index.html', {"activities": activities})
    else:
        return render(request, 'pages/matchmaking/ask_location.html', {})


class ActivityFormViewCreate(LoginRequiredMixin, CreateView):
    template_name = 'activity/create.html'
    form_class = ActivityForm
    success_url = '/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['users'].queryset = get_waiting_users(self.request.user)
        return form

    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super(ActivityFormViewCreate, self).form_valid(form)


class ActivityFormViewUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'activity/create.html'
    form_class = ActivityForm
    success_url = '/'
    model = ActivityModel


class ActivityDetailView(LoginRequiredMixin, generic.DetailView):
    model = Activity
    template_name = 'activity/view.html'

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data(**kwargs)

        # Reverse Geocode to get the street, the city and the country names
        context['coords'] = Geocoder.reverse_geocode(context['activity'].position.y, context['activity'].position.x)
        # Logged User informations
        context['user'] = self.request.user
        # Authentication params for Disqus
        # /!\ django-disqus authentication params not works - bad signature /!\
        message_dict = {'id': self.request.user.id, 'username': self.request.user.username,
                        'email': self.request.user.email}
        message = base64.b64encode(bytes(json.dumps(message_dict), 'utf-8'))
        d = datetime.utcnow()
        timestamp = calendar.timegm(d.utctimetuple())
        signature_msg = message.decode('utf-8') + " " + str(timestamp)
        signature = hmac.new(bytes(DISQUS_SECRET_KEY, 'utf-8'), bytes(signature_msg, 'utf-8'), 'sha1')
        context['disqus_auth'] = message.decode("utf-8") + ' ' + signature.hexdigest() + ' ' + str(timestamp)

        return context
