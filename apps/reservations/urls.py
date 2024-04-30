from django.urls import path
from .views import (ListReservationsView, PaymentResultView, OrderConfirmView, OrderCreateView)

app_name = 'reservations'

urlpatterns = [
    path('', ListReservationsView.as_view(), name='list'),
    path('checkout/<int:room_id>', OrderCreateView.as_view(), name='checkout'),
    path('payment/', OrderConfirmView.as_view(), name='payment'),
    path('result/', PaymentResultView.as_view(), name='payment_result'),
]
