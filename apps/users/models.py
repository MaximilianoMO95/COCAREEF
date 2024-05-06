from django.contrib.auth.models import (AbstractUser)
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(_('first_name'), max_length=30, blank=False)
    last_name = models.CharField(_('last_name'), max_length=30, blank=False)

    class Meta:
        permissions = [
            ('can_view_admin_panel', '[Custom] Can view admin panel'),
        ]


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    rut  = models.CharField(max_length=15, blank=False)
    phone_number = models.CharField(_('phone_numer'), max_length=20, blank=True)

    class Meta:
        permissions = [
            ('can_view_employee', '[Custom] Can view employee.'),
            ('can_add_employee', '[Custom] Can add a new employee.'),
            ('can_change_employee', '[Custom] Can change a employee.'),
        ]


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    dni = models.CharField(max_length=15, blank=False)
