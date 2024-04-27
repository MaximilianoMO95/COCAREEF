from django.contrib.auth.models import (AbstractUser)
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, verbose_name='Nombre', blank=False)
    last_name = models.CharField(max_length=30, verbose_name='Apellido', blank=False)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=15, verbose_name='DNI', blank=False)
