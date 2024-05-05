from django.core import signing
from django.db import models
from datetime import date

from django.utils import timezone

from apps.rooms.models import Room
from apps.users.models import User

class ReservationPaymentStatus(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ReservationQuerySet(models.QuerySet):
    def is_room_available(self, room: Room, check_in_date: date, days_of_stay: int) -> bool:
        check_out_date = check_in_date + timezone.timedelta(days=days_of_stay)
        overlapping_reservations = self.filter(
            room=room,
            start_date__lt=check_out_date,
            start_date__gte=check_in_date
        )

        is_available = not overlapping_reservations.exists()
        return is_available


    def delete_expired_reservations(self):
        # TODO: edge-case: the user is paying during scheduled deletation
        # posible solution: Add some field called "is_user_paying" every timee the user enter to the payment form
        expired_reservations = Reservation.objects.filter(is_reservation_expired=True)
        expired_reservations.delete()


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    days_of_stay = models.PositiveIntegerField(default=1)
    deposit_percentage = models.PositiveSmallIntegerField(default=30)
    payment_status = models.ForeignKey(ReservationPaymentStatus, to_field='code', on_delete=models.PROTECT, default='NP')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ReservationQuerySet.as_manager()

    def is_fully_paid(self) -> bool:
        return (self.payment_status.code == 'FP')


    def is_expired(self, timeout_period) -> bool:
        timeout_period = timezone.timedelta(hours=24)
        diff = timezone.now() - self.created_at

        return (diff > timeout_period)


    def update_payment_status(self, code: str) -> None:
        try:
            payment_status = ReservationPaymentStatus.objects.get(code=code)
        except ReservationPaymentStatus.DoesNotExist:
            raise ValueError(f"Payment status with code '{code}' does not exist.")

        self.payment_status = payment_status
        if payment_status.code == 'FP':
            self.deposit_percentage = 100

        self.save()


    def calc_total_amount(self) -> int:
        total: int = self.room.price * self.days_of_stay
        return total


    def calc_deposit_amount(self) -> int:
        total: int = self.calc_total_amount() * self.deposit_percentage
        result = int(total / 100)

        return result


    def calc_remaining_amount(self) -> int:
        if self.payment_status.code == 'NP':
            total = self.calc_total_amount()
            return total

        deposit_amount = self.calc_deposit_amount()
        amount_paid = (deposit_amount * self.deposit_percentage) / 100

        remaining_amount = int(deposit_amount - amount_paid)
        return remaining_amount


    @staticmethod
    def gen_qrcode_url(request, reservation_id: int|str) -> str:
        signed_data = signing.dumps(reservation_id)
        host = request.META['HTTP_HOST']

        url = f'{host}/reservations/details?reservation={signed_data}'
        return url
