from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import (UserLoginForm)
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import TemplateView



class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Credenciales invalidadas")  
        return response
   
class VistaAdminView(TemplateView):
    template_name = 'users/vistaadmin.html'

