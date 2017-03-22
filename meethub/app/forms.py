from django import forms
from django.contrib.gis import forms as gis_form
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Activity
from .widgets import UserCarouselMultiSelectWidget,Html5DateTime
from django.forms.widgets import DateTimeInput

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            'title',
            'description',
            'date_time',
            'position',
            'min_participants',
            'max_participants',
            'users',
            'admin'
        )


        widgets = {
            "users": UserCarouselMultiSelectWidget(),
            "position": GooglePointFieldWidget
        }





