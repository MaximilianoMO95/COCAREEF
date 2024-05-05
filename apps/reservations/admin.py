from django.contrib import admin

from .models import (Reservation, ReservationPaymentStatus)

admin.site.register(Reservation)
admin.site.register(ReservationPaymentStatus)
