from django.db import models

from apps.rooms.models import Room
from apps.users.models import User

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    days_of_stay = models.PositiveIntegerField()

    is_paid = models.BooleanField(default=False)

    def total_amount(self):
        percent = 0.3
        result = (self.room.price * self.days_of_stay) * percent

        return int(result)
