from django.urls import path
from .views import (DetailsReservationView, EditReservationView, ListReservationsView, PaymentResultView, OrderConfirmView, OrderCreateView, delete_reservation)

app_name = 'reservations'

urlpatterns = [
    path('', ListReservationsView.as_view(), name='list'),
    path('checkout/<int:room_id>', OrderCreateView.as_view(), name='checkout'),
    path('payment/', OrderConfirmView.as_view(), name='payment'),
    path('payment/status/', PaymentResultView.as_view(), name='payment_status'),
    path('edit/<int:reservation_id>', EditReservationView.as_view(), name='edit'),
    path('delete/<int:reservation_id>', delete_reservation, name='delete'),

    path('details/<int:id>', DetailsReservationView.as_view(), name='details'),
    path('details/', DetailsReservationView.as_view(), name='details'),
]
