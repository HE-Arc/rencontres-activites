from django import forms

from .models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            'title',
            'description',
            'date_time',
            'latitude',
            'longitude',
            'min_participants',
            'max_participants',
            'admin',
            'users'
        )

        widgets = {
            'latitude' : forms.HiddenInput(),
            'longitude': forms.HiddenInput()
        }
