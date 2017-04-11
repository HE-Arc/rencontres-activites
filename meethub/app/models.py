from django.contrib.auth.models import User
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.db import models
from django.contrib.gis.db import models as gmodels
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.geos import Point


def get_activities_near(lat, long):
    location = Point(float(long), float(lat))
    return Activity.objects \
        .filter(position__distance_lte=(location, D(km=10))) \
        .annotate(distance=Distance('position', location)) \
        .order_by('distance')


def get_waiting_users(user_to_recommend):
    """
    Returns a list of waiting users who arent near the event
    :param user_to_recommend_friends: the user who receives the recommandation of friends
    :return: a collection of users
    """

    # TODO: return some friends and last seen users
    return User.objects.all()


class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    position = gmodels.PointField(null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    min_participants = models.IntegerField()
    max_participants = models.IntegerField()
    admin = models.ForeignKey(User, related_name="admin")
    tags = models.ManyToManyField('Tag')
    users = models.ManyToManyField(User, related_name="participants")

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return str(self.name)


class WaitingUser(models.Model):
    users = models.ManyToManyField(User)
    tag = models.ForeignKey('Tag')

    # Time since last refresh of waiting user
    started_at = models.DateTimeField(null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='uploads/img/avatars')
    birthdate = models.DateField(blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
