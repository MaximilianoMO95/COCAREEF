from django.contrib.auth.forms import AuthenticationForm 
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee

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
    email = forms.EmailField(label='Email')  # Agregar campo de email al formulario

    class Meta:
        model = Employee
        fields = ['user', 'email']  # Lista de campos que deseas editar