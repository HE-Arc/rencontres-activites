from django.core import serializers
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


    activities = Activity.objects.all();
    context['activities'] =  activities;
    return render(request,'pages/dashboard.html', context)

class ActivityFormViewCreate(CreateView):
    template_name = 'activity/create.html'
    form_class = ActivityForm
    success_url = '/'

class ActivityFormViewUpdate(UpdateView):
    template_name = 'activity/create.html'
    form_class = ActivityForm
    success_url = '/'
    model = ActivityModel

class ActivityDetailView(generic.DetailView):
    model = Activity
    template_name = 'activity/index.html'
