from django.urls import path
from .views import (ListReservationsView, PaymentResultView, CheckoutConfirmView, CheckoutCreateView)

app_name = 'reservations'

urlpatterns = [
    path('checkout/<int:room_id>', CheckoutCreateView.as_view(), name='checkout'),
    path('payment/', CheckoutConfirmView.as_view(), name='payment'),
    path('result/', PaymentResultView.as_view(), name='payment_result'),
    path('list/', ListReservationsView.as_view(), name='list_reservations'),
]
