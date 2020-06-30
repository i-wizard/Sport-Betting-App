from django import forms

from support.models import Support


class IssueForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = '__all__'
        error_messages = {
            'username': {
                'required': "Please enter your fullname.",
            },
            'phone': {
                'required': 'Please enter your phone number.'
            },
            'email': {
                'required': 'Please enter your email address.'
            },
            'message': {
                'required': 'Please state your issue.'
            }
        }
