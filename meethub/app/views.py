from django.core import serializers
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect

from .models import Activity as ActivityModel
from .models import Activity
from .models import UserProfile
from django.http import HttpResponse
from var_dump import var_dump

from datetime import datetime, timedelta, time

from .forms import ActivityForm, UserForm, ProfileForm
from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext as _


def index(request):
    return render(request, 'pages/index.html')

@login_required
def dashboard(request):
    today = datetime.now()
    u = request.user
    context = {}
    # Get the informations of the logged user

    # Get the three latest activities done by the user
    activities_done_by_the_user = u.participants.filter(date__lte=today).order_by('-date')[:3]
    # Get the three next activities of the user
    next_activities_of_the_user = u.participants.filter(date__gte=today).order_by('date')[:3]
    # Get the first 10 upcoming activities.
    upcoming_activities = Activity.objects.filter(date__gte=today).order_by('date')[:10]

    # Give the informations to the view
    context['activities_done'] =  activities_done_by_the_user
    context['next_activities'] = next_activities_of_the_user
    context['upcoming_activities'] = upcoming_activities

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


class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'user/profile.html'
    context_object_name = 'user'
    today = datetime.now()

    def activities_done(self):
        return self.object.participants.filter(date__lte=self.today).order_by('-date')

    def next_activities(self):
        return self.object.participants.filter(date__gte=self.today).order_by('date')

    def age(self):
        return self.today.year - self.object.userprofile.birthdate.year - ((self.today.month, self.today.day) < (self.object.userprofile.birthdate.month, self.object.userprofile.birthdate.day))


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Votre profil a bien été mis à jour !'))
            return redirect('profile', pk=request.user.id)
        else:
            messages.error(request, _('Corrigez les erreurs...'))

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'user/update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
