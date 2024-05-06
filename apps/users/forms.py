from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import (User, Employee)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label=_('First Name'), max_length=30, required=True, help_text=_('Required. Please type your name.'))
    last_name = forms.CharField(label=_('Last Name'), max_length=30, required=True, help_text=_('Required. Please type your last name.'))
    dni = forms.CharField(max_length=15, required=True, help_text=_('Required. Please type your dni.'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'dni')
        labels = {
            'username': _('Username'),
            'password1': _('Password'),
            'password2': _('Confirm Password')
        }


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': _('username'),
            'password': _('password'),
        }


class EmployeeRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label=_('First Name'), max_length=30, required=True, help_text=_('Required. Please type your name.'))
    last_name = forms.CharField(label=_('Last Name'), max_length=30, required=True, help_text=_('Required. Please type your last name.'))
    rut = forms.CharField(max_length=15, required=True, help_text='Required. Please type your RUT.')
    phone_number = forms.CharField(label=_('Phone Number'), max_length=9, required=True, help_text='Required. Please type your phone number.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'rut', 'phone_number')
        labels = {
            'username': _('Username'),
            'password1': _('Password'),
            'password2': _('Confirm Password')
        }


class EmployeeEditForm(forms.ModelForm):
    email = forms.EmailField()
    phone_number = forms.CharField(label=_('Phone Number'))

    class Meta:
        model = Employee
        fields = ['user', 'email', 'phone_number']
        labels = { 'user': _('User') }
