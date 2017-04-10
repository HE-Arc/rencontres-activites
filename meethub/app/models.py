from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.db import models
from django.contrib.gis.db import models as gmodels
from django.contrib.gis.geos import Point

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

    @staticmethod
    def get_activities_near(lat, long):
        location = GEOSGeometry('POINT(%s %s)' % (lat,long), srid=4326)
        return Activity.objects.filter(position__distance_lte=(location, D(m=5)))

    @staticmethod
    def get_waiting_users(user_to_recommend_friends):
        """
        Returns a list of waiting users who arent near the event
        :param user_to_recommend_friends: the user who receives the recommandation of friends
        :return: a collection of users
        """

        # TODO: return some friends and last seen users
        return User.objects.all()


class Tag(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return str(self.name)


class WaitingUser(models.Model):
    users = models.ManyToManyField(User)
    tag = models.ForeignKey('Tag')

