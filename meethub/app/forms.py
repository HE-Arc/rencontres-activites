from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.contrib.gis import forms as gis_form
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Activity,User
from .widgets import UserCarouselMultiSelectWidget, Html5Date, Html5Time

class ActivityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['users'].required = False

    class Meta:
        model = Activity
        fields = (
            'title',
            'description',
            'date',
            'time',
            'position',
            'min_participants',
            'max_participants',
            'users',
            'tags'
        )

        widgets = {
            "users": UserCarouselMultiSelectWidget(),
            "position": GooglePointFieldWidget,
            'date': Html5Date,
            "time": Html5Time
        }




