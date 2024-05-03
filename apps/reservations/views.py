from datetime import date
from urllib.parse import parse_qs
from django.http.response import HttpResponseForbidden, JsonResponse
from django.shortcuts import (redirect, render, get_object_or_404)
from django.views import View
from django.contrib.admin.options import method_decorator
from django.contrib.auth.views import login_required
from django.contrib.sites.shortcuts import get_current_site
import django.http as http
from django.views.generic import ListView

from apps.rooms.models import Room
from apps.webpay.views import WebpayAPI
from .models import Reservation
from .forms import (OrderCreateForm, ReservationForm)

@method_decorator(login_required, name='dispatch')
class ListReservationsView(ListView):
    model = Reservation
    template_name = 'reservations/admin/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class EditReservationView(View):
    template_name = 'reservations/admin/update.html'

    def get(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)
        form = ReservationForm(instance=reservation)
        return render(request, self.template_name, { 'form': form, 'reservation_id': reservation_id })


    def post(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservations:list')

        return render(request, self.template_name, { 'form': form, 'reservation_id': reservation.id })


@method_decorator(login_required, name='dispatch')
class OrderCreateView(View):
    template_name = 'reservations/checkout.html'

    def get(self, request, room_id):
        form = OrderCreateForm(
            initial={ 'days_of_stay': 1 }
        )
        room = get_object_or_404(Room, id=room_id)
        return render(request, self.template_name, { 'form': form, 'room': room })


    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            start_date: date = form.cleaned_data['start_date']
            total_days: int = form.cleaned_data['days_of_stay']

            is_room_available = Reservation.objects.is_room_available(room, start_date, total_days);
            if is_room_available:
                reservation = book_room(
                    request,
                    room_id,
                    form.cleaned_data['start_date'],
                    form.cleaned_data['days_of_stay'],
                )
                if reservation:
                    request.session['reservation_id'] = reservation.pk
                    return redirect('reservations:payment')
            else:
                form.add_error('start_date', 'La habitacion no esta disponible para esa fecha.')

        return render(request, self.template_name, { 'form': form, 'room': room })


# TODO: Add session id
# TODO: Check if room is not already booked
@method_decorator(login_required, name='dispatch')
class OrderConfirmView(View):
    template_name = 'reservations/confirm-checkout.html'

    def get(self, request):
        order_id = 'hotel-reef-order'
        reservation_id = request.session['reservation_id']
        reservation = Reservation.objects.get(pk=reservation_id)
        order_total_amount = reservation.total_amount()

        return_url = request.scheme + '://' + get_current_site(request).domain + '/reservations/payment/status'
        session_id = request.session.session_key

        webpay = WebpayAPI()
        response_data = webpay.create_transaction(order_total_amount, order_id, session_id, return_url)

        if response_data:
            url = response_data['url']
            token = response_data['token']

            return render(request, self.template_name, { 'url': url, 'token_ws': token, 'total_amount': order_total_amount })
        else:
            return http.JsonResponse({ 'message': 'Failed to create Webpay transaction' })


    def delete(self, request):
        reservation_id = request.session['reservation_id']
        reservation = get_object_or_404(Reservation, id=reservation_id)

        response = JsonResponse({ 'message': 'failed to cancel reservation' }, status=400)
        if request.user == reservation.user:
            reservation.delete()
            del request.session['reservation_id']
            response = JsonResponse({ 'message': 'reservation canceled' }, status=200)
            response['HX-Redirect'] = '/rooms'

        return response


@method_decorator(login_required, name='dispatch')
class PaymentResultView(View):
    template_name = 'reservations/payment_status.html'

    def get(self, request):
        webpay = WebpayAPI()
        query_params = parse_qs(request.GET.urlencode())

        reject_token = 'TBK_TOKEN'
        if reject_token in query_params:
            return render(request, self.template_name, { 'pay_status': 'CANCELADO' })

        token = 'token_ws'
        if token in query_params:
            token = query_params[token][0]

        response_data = webpay.commit_transaction(token)
        if response_data:
            pay_status = response_data['status']
            return render(request, self.template_name, { 'pay_status': pay_status })
        else:
            return http.JsonResponse('Failed to confirm Webpay transaction')


def book_room(request, room_id, start_date, days_of_stay) -> Reservation | None:
    # TODO: check if room is available
    room_instance = Room.objects.get(id=room_id)

    if room_instance:
        reservation, _ = Reservation.objects.get_or_create(
            user = request.user,
            room = room_instance,
            start_date = start_date,
            days_of_stay = days_of_stay,
            is_paid = False,
        )
        reservation.save()

        return reservation


@login_required
def delete_reservation(request, reservation_id):
    room = Reservation.objects.get(id=reservation_id)
    room.delete()

    return redirect('reservations:list')
