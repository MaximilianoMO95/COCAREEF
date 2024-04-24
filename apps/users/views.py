from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect


from .forms import UserRegistrationForm
from .models import Customer

class UserRegistrationView(View):
    template_name = 'users/signin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')

        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')

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

            return redirect('index')

        return render(request, self.template_name, {'form': form})
