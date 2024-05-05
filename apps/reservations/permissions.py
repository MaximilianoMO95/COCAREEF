from django.contrib.auth.models import (Permission, Group)
from django.contrib.contenttypes.models import ContentType

from apps.reservations.models import Reservation

# EMPLOYEE RELATED PERMISSIONS
content_type = ContentType.objects.get_for_model(Reservation)
employee_group, created = Group.objects.get_or_create(name='employee')

can_view_reservation, _ = Permission.objects.get_or_create(
    codename='can_view_reservation',
    name='[Custom] Can view a reservation',
    content_type=content_type,
)
can_add_reservation, _ = Permission.objects.get_or_create(
    codename='can_add_reservation',
    name='[Custom] Can add a reservation',
    content_type=content_type,
)
can_delete_reservation, _ = Permission.objects.get_or_create(
    codename='can_delete_reservation',
    name='[Custom] Can delete a reservation',
    content_type=content_type,
)
can_change_reservation, _ = Permission.objects.get_or_create(
    codename='can_change_reservation',
    name='[Custom] Can change a reservation',
    content_type=content_type,
)
