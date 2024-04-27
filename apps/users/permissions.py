from django.contrib.auth.models import (Permission, Group)
from django.contrib.contenttypes.models import ContentType

from .models import Customer

customer_content_type = ContentType.objects.get_for_model(Customer)
customer_group, created = Group.objects.get_or_create(name='customer')

edit_customer_profile_permission, _ = Permission.objects.get_or_create(
    codename='edit_customer_profile',
    name='Can edit customer profile',
    content_type=customer_content_type,
)

customer_group.permissions.add(edit_customer_profile_permission)
