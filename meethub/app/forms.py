from django import forms
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Activity
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
