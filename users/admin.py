from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import User


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'phone', 'calling_code', 'is_staff', 'is_moderator', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm

    list_display = (
        'username', 'email', 'calling_code', 'phone', 'referred', 'is_staff', 'is_moderator', 'is_active')
    list_filter = ('is_staff', 'is_moderator',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'calling_code', 'phone', 'password', 'profile_image', 'referral_code', 'referred',)}),
        ('Permissions', {'fields': ('is_staff', 'is_moderator', 'is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'calling_code', 'phone', 'password1',
                'password2')}
         ),
    )
    search_fields = ('username', 'phone',)
    ordering = ('username', 'phone',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

