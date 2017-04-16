import base64
import calendar
import hmac
import json
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count
from django.db.models import F
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404

from django.core import serializers
from django.forms import forms

from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic import CreateView
from django.views.generic import UpdateView
from pygeocoder import Geocoder

from secret import DISQUS_SECRET_KEY
from .forms import ActivityForm, ChooseTagsForm
from .forms import UserForm, ProfileForm
from .models import Activity, get_activities_near, get_waiting_users, WaitingUser, Tag, Invitation
from .models import Activity as ActivityModel
from secret import *
from friendship.models import Friend, Follow
from friendship.models import FriendshipRequest


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

    # Get the friend's requests for the authenticated user
    friendshipsRequests = FriendshipRequest.objects.filter(to_user=u).all()

    # Give the informations to the view
    context['activities_done'] = activities_done_by_the_user
    context['next_activities'] = next_activities_of_the_user
    context['upcoming_activities'] = upcoming_activities

    context['requests'] = friendshipsRequests

    context['api_key_map'] = "AIzaSyD48NmCV_kXSHmaGQSdEGojD7vkcRcNqME"

    activities = Activity.objects.all()
    context['activities'] = activities
    return render(request, 'pages/dashboard.html', context)


@login_required
def matchmaking(request, lat=None, long=None):
    tags_query = request.GET.getlist('tags')

    if lat and long and tags_query:

        tags = Tag.objects.filter(name__in=tags_query)

        for tag in tags:
            waiting, _ = WaitingUser.objects.get_or_create(user=request.user, tag=tag)
            waiting.started_at = datetime.now()
            waiting.save()

        # Gets activities near the users with open places
        activities = get_activities_near(lat, long) \
            .filter(tags__activity__tags__in=tags) \
            .filter(date__gte=datetime.now().date()) \
            .annotate(users_count=Count("users")) \
            .filter(users_count__lt=F("max_participants"))

        return render(request, 'pages/matchmaking/index.html', {
            "activities": activities,
            "form": ChooseTagsForm(),
            "invitations": request.user.invitations.all(),
            "activities_where_invited": map(lambda e: e.event, request.user.invitations.all())
        })
    elif lat and long:
        return render(request, 'pages/matchmaking/ask_tags.html', {"form": ChooseTagsForm()})
    else:
        return render(request, 'pages/matchmaking/ask_location.html', {})


class ActivityFormViewCreate(LoginRequiredMixin, CreateView):
    template_name = 'activity/create.html'
    form_class = ActivityForm
    success_url = '/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['users'].widget.choices = Friend.objects.friends(self.request.user)
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
        # context['coords'] = Geocoder.reverse_geocode(context['activity'].position.y, context['activity'].position.x)
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

    def post(self, request, pk):
        activity = Activity.objects.get(pk=(int(pk)))
        if (request.POST.get('join_id')):
            user = User.objects.get(pk=int(request.POST.get('join_id')))
            activity.users.add(user)
        else:
            user = User.objects.get(pk=int(request.POST.get('quit_id')))
            activity.users.remove(user)
        return redirect(request.META.get('HTTP_REFERER'))


class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'user/profile.html'
    context_object_name = 'user'
    today = datetime.now()

    def isAFriend(self):
        return Friend.objects.are_friends(self.object, self.request.user)

    def isARequestPending(self):
        return FriendshipRequest.objects.select_related('from_user', 'to_user').filter(to_user=self.object,
                                                                                       from_user=self.request.user).all().count()

    def friends(self):
        return Friend.objects.friends(self.object)

    def activities_done(self):
        return self.object.participants.filter(date__lte=self.today).order_by('-date')

    def next_activities(self):
        return self.object.participants.filter(date__gte=self.today).order_by('date')

    def age(self):
        return self.today.year - self.object.userprofile.birthdate.year - ((self.today.month, self.today.day) < (
        self.object.userprofile.birthdate.month, self.object.userprofile.birthdate.day))


class AddUserAsAFriend(LoginRequiredMixin, generic.View):
    model = Friend

    def post(self, request):
        other_user = User.objects.get(pk=int(request.POST.get('user_id')))
        Friend.objects.add_friend(
            request.user,  # The sender
            other_user,  # The recipient
            message='Hi! I would like to add you')  # This message is optional
        messages.info(request, "Votre demande a été faite !")
        return redirect(request.META.get('HTTP_REFERER'))


class ManageFriendshipRequest(LoginRequiredMixin, generic.View):
    model = FriendshipRequest

    def post(self, request):
        friend_request = FriendshipRequest.objects.get(pk=int(request.POST.get('request_id')))

        if request.POST.get('action') == 'accept':
            friend_request.accept()
            message = friend_request.from_user.username + " est maintenant votre ami(e) !"

        elif request.POST.get('action') == 'reject':
            friend_request.delete()
            message = friend_request.from_user.username + " n'est pas votre ami !"

        messages.info(request, message)
        return redirect(request.META.get('HTTP_REFERER'))


class RemoveFriend(LoginRequiredMixin, generic.View):
    model = Friend

    def post(self, request):
        Friend.objects.remove_friend(request.user, User.objects.get(pk=int(request.POST.get('friend_id'))))
        messages.info(request, "Vous n'êtes plus amis !")
        return redirect(request.META.get('HTTP_REFERER'))


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


@login_required()
def invite_user(request, user_to_invite_pk, event_pk):
    event = get_object_or_404(Activity, id=event_pk)

    if event.admin == request.user:
        user_to_invite = get_object_or_404(User, id=user_to_invite_pk)

        invitation, _ = Invitation.objects.get_or_create(
            event=event,
            to_user=user_to_invite
        )
        invitation.expires_in = datetime.now() + timedelta(minutes=30)
        invitation.save()

        user_to_invite.invitations.add(invitation)

        return HttpResponseRedirect(reverse("activity", kwargs={"pk": event.id}))
    else:
        return HttpResponse('Unauthorized', status=401)
