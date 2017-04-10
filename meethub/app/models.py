from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField
from django.contrib.gis.db import models as gmodels


class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    position = gmodels.PointField(null=True)
    date_time = models.DateTimeField()
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
        return self.name

class WaitingUser(models.Model):
    users = models.ManyToManyField(User)
    tag = models.ForeignKey('Tag')
