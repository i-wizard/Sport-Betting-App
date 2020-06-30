from django import forms

from .models import User


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Please enter your email address.")

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("User with this e-mail address does not exist.")

        return cleaned_data


class ForgotResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    retype_password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password').lower()
        retype_password = cleaned_data.get('retype_password').lower()

        if not password:
            raise forms.ValidationError("Please enter your password")

        if len(password) < 6:
            raise forms.ValidationError("Password must be above 6 characters.")

        if retype_password != password:
            raise forms.ValidationError("Password and retype password do not match")

        return cleaned_data

#
#
# class UserProfileUpdateForm(forms.Form):
#     password = forms.CharField(required=False)
#     retype_password = forms.CharField(required=False)
#     phone = forms.CharField(min_length=11, max_length=11,
#                             error_messages={'min_length': 'Please enter a valid phone number.',
#                                             'max_length': 'Please enter a valid phone number.'})
#     bank_name = forms.CharField(error_messages={'required': 'Please enter bank name.'})
#     bank_account_name = forms.CharField(error_messages={'required': 'Please enter bank account name.'})
#     bank_account_number = forms.CharField(min_length=10, max_length=11,
#                                           error_messages={'min_length': 'Bank account number is not valid',
#                                                           'max_length': 'Bank account number is not valid'})
#
#     def clean(self):
#         cleaned_data = self.cleaned_data
#         password = cleaned_data.get('password')
#         retype_password = cleaned_data.get('retype_password')
#
#         if password:
#             if retype_password != password:
#                 raise forms.ValidationError("Password and retype password do not match")
#
#         return cleaned_data
#
