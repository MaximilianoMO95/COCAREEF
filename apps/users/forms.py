from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm)

from .models import (User, Employee)
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Ingrese su nombre.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Ingrese su apellido.')
    dni = forms.CharField(max_length=15, required=True, help_text='Required. Ingrese su dni.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'dni')


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class EmployeeRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Ingrese su nombre.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Ingrese su apellido.')
    rut = forms.CharField(max_length=15, required=True, help_text='Required. Ingrese su RUT.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'rut')


class EmployeeEditForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Employee
        fields = ['user', 'email']
