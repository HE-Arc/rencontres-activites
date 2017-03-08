from django.core import serializers
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views import View, generic

from .models import Activity as ActivityModel
from .models import Activity

from .forms import ActivityForm

def index(request):
    return render(request,'pages/dashboard.html')

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
    context_object_name = 'activity'
