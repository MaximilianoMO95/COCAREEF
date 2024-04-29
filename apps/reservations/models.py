from django.db import models

from apps.rooms.models import Room
from apps.users.models import User

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    days_of_stay = models.PositiveIntegerField()
