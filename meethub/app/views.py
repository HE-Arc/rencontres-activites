from django.core import serializers
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Activity as ActivityModel
from .models import Activity
from django.http import HttpResponse
from var_dump import var_dump

from datetime import datetime, timedelta, time

from .forms import ActivityForm



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
    context['activities_done'] =  activities_done_by_the_user;
    context['next_activities'] = next_activities_of_the_user;
    context['upcoming_activities'] = upcoming_activities;

    context['api_key_map'] = "AIzaSyD48NmCV_kXSHmaGQSdEGojD7vkcRcNqME"

    return render(request,'pages/dashboard.html', context)

class ActivityFormViewCreate(LoginRequiredMixin, CreateView):
    template_name = 'activity/create.html'
    form_class = ActivityForm
    success_url = '/'

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
    template_name = 'activity/index.html'
    context_object_name = 'activity'
