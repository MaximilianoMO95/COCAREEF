from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from .forms import (UserLoginForm)
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import EmployeeRegistrationForm

from django.contrib.auth import login
from django.views import View
from django.contrib.auth.models import Group
from .models import Employee
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.views.generic import ListView
from .forms import EmployeeEditForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Credenciales invalidadas")  
        return response
   
class VistaAdminView(TemplateView):
    template_name = 'users/vistaadmin.html'


class EmployeeRegistrationView(View):
    template_name = 'users/employee.html'

    def get(self, request):
        form = EmployeeRegistrationForm()
        return render(request, self.template_name, { 'form': form })

    def post(self, request):
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

           
            
            employee_group, _ = Group.objects.get_or_create(name='employee')
            user.groups.add(employee_group)

            employee = Employee.objects.create(
                user=user,
                rut=form.cleaned_data['rut']
               
            )
            employee.save()
          
            login(request, user)

            return redirect('users:employee_list')

        return render(request, self.template_name, { 'form': form })
    
class EmployeeListView(ListView):
    template_name = 'users/employee_list.html'
    model = Employee
    context_object_name = 'employee_list'

    def get_queryset(self):
        return Employee.objects.all()


    
class EmployeeEditView(View):
    template_name = 'users/employee_edit.html'

    def get(self, request, rut):
        employee = Employee.objects.get(rut=rut)
        form = EmployeeEditForm(instance=employee)
        return render(request, self.template_name, {'form': form, 'employee': employee})

    def post(self, request, rut):
        employee = Employee.objects.get(rut=rut)
        form = EmployeeEditForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('users:employee_list')
        return render(request, self.template_name, {'form': form, 'employee': employee})
