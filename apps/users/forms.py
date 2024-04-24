from django import forms
from django.contrib.auth.forms import (UserCreationForm)

from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Ingresa tu nombre.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Ingresa tu apellido.')
    dni = forms.CharField(max_length=60)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'dni')
