from django import forms

from core.models import Slider
from stack.models import Team, Event
from users.models import User


class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)
        error_messages = {
            'name': {
                'required': "Please enter team name.",
                'unique': "Team already exist.",
            },
        }


class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_name',)
        error_messages = {
            'event_name': {
                'required': "Please enter event name.",
                'unique': "Event already exist.",
            },
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ('image',)


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone', 'email', 'username', 'password', 'is_moderator')
        error_messages = {
            'username': {
                'required': "Please enter username.",
                'unique': "Username already in use.",
            },
            'phone': {
                'required': 'Please provide a phone number.',
                'unique': 'A user with this phone number already exist.'
            },
            'email': {
                'required': 'Please provide email address.',
                'unique': 'A user with this email address already exist.'
            }
        }


class GamesSettingForm(forms.Form):
    min_user_limit = forms.IntegerField(required=False)
    num_smart_users = forms.IntegerField(required=False)
    num_jackpot_winners = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        min_user_limit = int(cleaned_data.get('min_user_limit'))
        num_smart_users = int(cleaned_data.get('num_smart_users'))
        num_jackpot_winners = int(cleaned_data.get('num_jackpot_winners'))

        if num_smart_users < 1:
            raise forms.ValidationError('Please enter the number of smart users')

        if min_user_limit < 1:
            raise forms.ValidationError('Please enter the the minimum limit for super users to be added to a game')

        if num_jackpot_winners < 1:
            raise forms.ValidationError('Please enter the number of jackpot winners')

        return cleaned_data
