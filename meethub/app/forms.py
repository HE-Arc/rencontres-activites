from django import forms
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Activity, User, UserProfile, Tag
from .models import Activity
from .widgets import UserCarouselMultiSelectWidget, Html5Date, Html5Time


class ChooseTagsForm(forms.Form):

    tags = forms.MultipleChoiceField(choices=[(tag.name, tag.name) for tag in Tag.objects.all()])


class ActivityForm(forms.ModelForm):
    date_time = forms.SplitDateTimeField(input_time_formats=['%H:%M'], input_date_formats=['%d/%m/%Y'])
    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget.widgets[0].attrs.update({'class' : 'datepicker', 'placeholder' : 'Date'}) #assign the class date to the datefield
        self.fields['date_time'].widget.widgets[1].attrs.update({'class' : 'clockpicker', 'placeholder': 'Heure'})
        self.fields['users'].required = False

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
            'tags'
        )

        widgets = {
            "users": UserCarouselMultiSelectWidget(),
            "position": GooglePointFieldWidget,
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'image', 'birthdate')

        widgets = {
            "birthdate": Html5Date,
        }
