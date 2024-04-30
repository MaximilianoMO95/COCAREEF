from urllib.parse import parse_qs
from django.shortcuts import (HttpResponseRedirect, redirect, render, get_object_or_404)
from django.views import View
from django.contrib.admin.options import method_decorator
from django.contrib.auth.views import login_required
from django.contrib.sites.shortcuts import get_current_site
import django.http as http
from django.views.generic import ListView

from apps.rooms.models import Room
from apps.webpay.views import WebpayAPI
from .models import Reservation
from .forms import ReservationForm

#TODO: Clean up the mess
#TODO: Add required permisitions

@method_decorator(login_required, name='dispatch')
class ListReservationsView(ListView):
    model = Reservation
    template_name = 'reservations/admin/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditReservationView(View):
    template_name = 'reservations/admin/edit.html'


#@method_decorator(login_required, name='dispatch')
class OrderCreateView(View):
    template_name = 'reservations/checkout.html'

    def get(self, request, room_id):
        form = ReservationForm()
        room = get_object_or_404(Room, id=room_id)
        return render(request, self.template_name, { 'form': form, 'room': room })


    def post(self, request, room_id):
        form = ReservationForm(request.POST)

        if form.is_valid():
            # TODO: Check if room is available
            is_room_available = True;
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
                form.add_error(None, 'Room is not available.')

        room = get_object_or_404(Room, id=room_id)
        return render(request, self.template_name, { 'form': form, 'room': room })


# TODO: Add session id
# TODO: Check if room is not already booked
@method_decorator(login_required, name='dispatch')
class OrderConfirmView(View):
    template_name = 'payment/checkout.html'

    def get(self, request):
        order_id = 'hotel-reef-order-1234'
        reservation_pk = request.session['reservation_id'];
        reservation = Reservation.objects.get(pk=reservation_pk)
        order_total_amount = reservation.total_amount()

        return_url = request.scheme + '://' + get_current_site(request).domain + '/payment/result.html'
        session_id = request.session.session_key

        webpay = WebpayAPI()
        response_data = webpay.create_transaction(order_total_amount, order_id, session_id, return_url)

        if response_data:
            url = response_data['url']
            token = response_data['token']

            return render(request, self.template_name, { 'url': url, 'token_ws': token, 'total_amount': order_total_amount })
        else:
            return http.JsonResponse({ 'message': 'Failed to create Webpay transaction' })


@method_decorator(login_required, name='dispatch')
class PaymentResultView(View):
    template_name = 'reservations/payment_status.html'

    def get(self, request):
        webpay = WebpayAPI()
        query_params = parse_qs(request.GET.urlencode())

        reject_token = 'TBK_TOKEN'
        if reject_token in query_params:
            return render(request, self.template_name, { 'pay_status': 'PAGO CANCELADO' })

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
def remove_booked_room(request, room_id):
    room = Reservation.objects.get(id=room_id)
    room.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
