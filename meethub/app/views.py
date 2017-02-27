from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import UpdateView

from .forms import ActivityForm
from .models import Activity as ActivityModel


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