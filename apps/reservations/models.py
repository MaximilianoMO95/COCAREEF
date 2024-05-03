from django.db import models
from datetime import date, timedelta

from apps.rooms.models import Room
from apps.users.models import User

class ReservationQuerySet(models.QuerySet):
    def is_room_available(self, room: Room, check_in_date: date, days_of_stay: int) -> bool:
        check_out_date = check_in_date + timedelta(days=days_of_stay)
        overlapping_reservations = self.filter(
            room=room,
            start_date__lt=check_out_date,
            start_date__gte=check_in_date
        )

        is_available = not overlapping_reservations.exists()
        return is_available


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    days_of_stay = models.PositiveIntegerField(default=1)
    is_paid = models.BooleanField(default=False)

    objects = ReservationQuerySet.as_manager()

    def total_amount(self) -> int:
        percent = 0.3
        result = int((self.room.price * self.days_of_stay) * percent)

        return result
