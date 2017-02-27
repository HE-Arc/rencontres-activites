from django import forms

from .models import Activity


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
            'admin',
            'users'
        )
