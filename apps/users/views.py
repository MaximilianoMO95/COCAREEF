from django.views import View
from django.contrib.auth.views import LoginView, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import (ListView, TemplateView)

from .forms import (EmployeeEditForm, EmployeeRegistrationForm, UserRegistrationForm, UserLoginForm)
from .models import (Customer, Employee)

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('users:admin-panel')

        return reverse_lazy('rooms:catalogue')


    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('users:admin-panel')

            return redirect('rooms:catalogue')

        return super().dispatch(request, *args, **kwargs)


    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Credenciales invalidadas')
        return response


class AdminPanelView(TemplateView):
    template_name = 'users/admin/panel.html'


class UserRegistrationView(View):
    template_name = 'users/signin.html'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('users:admin-panel')

            return redirect('rooms:catalogue')

        form = UserRegistrationForm()
        return render(request, self.template_name, { 'form': form })

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            customer_group, _ = Group.objects.get_or_create(name='customer')
            user.groups.add(customer_group)

            customer = Customer(user=user)
            customer.save()

            login(request, user)

            return redirect('rooms:catalogue')

        return render(request, self.template_name, { 'form': form })


class EmployeeRegistrationView(View):
    template_name = 'users/admin/employee.html'

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
    model = Employee
    template_name = 'users/admin/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EmployeeEditView(View):
    template_name = 'users/admin/employee_edit.html'

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
