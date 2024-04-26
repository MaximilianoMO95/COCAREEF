from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, verbose_name='Nombre', blank=False)
    last_name = models.CharField(max_length=30, verbose_name='Apellido', blank=False)
    
    # Define related_name para evitar conflictos con los campos relacionales heredados
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

