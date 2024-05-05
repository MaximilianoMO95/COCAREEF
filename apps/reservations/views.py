from datetime import date
from urllib.parse import parse_qs
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.http.response import (Http404, JsonResponse)
from django.shortcuts import (redirect, render, get_object_or_404)
from django.utils import timezone
from django.views import View
from django.contrib.admin.options import method_decorator
from django.contrib.sites.shortcuts import get_current_site
import django.http as http
from django.views.generic import ListView
from django.views.generic.list import Paginator

from apps.rooms.models import Room
from apps.webpay.views import WebpayAPI
from .models import Reservation
from .forms import (OrderCreateForm, ReservationFilterForm, ReservationForm)

@method_decorator(login_required, name='dispatch')
class ListReservationsView(ListView):
    model = Reservation
    template_name = 'reservations/admin/list.html'
    filter_form = ReservationFilterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form(self.request.GET)

        paginator = Paginator(context['object_list'], 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context


    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')
        form = self.filter_form(self.request.GET)

        if form.is_valid():
            start_date_from = self.request.GET.get('start_date_from')
            if start_date_from:
                queryset = queryset.filter(start_date__gte=start_date_from)

            start_date_to = self.request.GET.get('start_date_to')
            if start_date_to:
                queryset = queryset.filter(start_date__lte=start_date_to)

        return queryset


@method_decorator(login_required, name='dispatch')
class CreateReservationView(View):
    template_name = 'reservations/admin/create.html'

    def get(self, request):
        form = ReservationForm()
        return render(request, self.template_name, { 'form': form })


    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            room: Room = form.cleaned_data['room']
            start_date: date = form.cleaned_data['start_date']
            total_days: int = form.cleaned_data['days_of_stay']

            is_room_available = Reservation.objects.is_room_available(room, start_date, total_days);
            if is_room_available:
                form.save()
                return redirect('reservations:list')
            else:
                form.add_error('start_date', 'La habitacion no esta disponible para esa fecha.')

        return render(request, self.template_name, { 'form': form })


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
        room = get_object_or_404(Room, id=room_id)
        threshold = timezone.now() - timezone.timedelta(hours=24)

        try:
            reservation = Reservation.objects.get(
                user=request.user,
                room=room,
                created_at__gte=threshold,
                payment_status__code = 'NP',
            )

            request.session['reservation_id'] = reservation.pk
            request.session.set_expiry(24 * 60 * 60)
            return redirect('reservations:payment')
        except Reservation.DoesNotExist: pass

        form = OrderCreateForm(initial={ 'days_of_stay': 1 })
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
                    request.session.set_expiry(24 * 60 * 60)

                    return redirect('reservations:payment')
            else:
                form.add_error('start_date', 'La habitacion no esta disponible para esa fecha.')

        return render(request, self.template_name, { 'form': form, 'room': room })


@method_decorator(login_required, name='dispatch')
class OrderConfirmView(View):
    template_name = 'reservations/confirm-checkout.html'

    def get(self, request):
        order_id = 'hotel-reef-order'
        reservation_id = request.session['reservation_id']
        reservation = Reservation.objects.get(pk=reservation_id)
        order_total_amount = reservation.calc_deposit_amount()

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
        bad_response = JsonResponse({ 'message': 'failed to cancel reservation' }, status=400)
        if 'reservation_id' not in request.session:
            return bad_response

        reservation_id = request.session['reservation_id']
        reservation = get_object_or_404(Reservation, id=reservation_id)
        if request.user != reservation.user:
            return bad_response

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
            reservation_id = request.session['reservation_id']
            qr_url = Reservation.gen_qrcode_url(request, reservation_id)

            reservation: Reservation = Reservation.objects.get(id=reservation_id)
            reservation.update_payment_status(code='PP')

            return render(request, self.template_name, { 'response_data': response_data, 'qr_url': qr_url })
        else:
            return http.JsonResponse('Failed to confirm Webpay transaction')


def book_room(request, room_id, start_date, days_of_stay) -> Reservation | None:
    room_instance = Room.objects.get(id=room_id)
    if room_instance:
        reservation, _ = Reservation.objects.get_or_create(
            user = request.user,
            room = room_instance,
            start_date = start_date,
            days_of_stay = days_of_stay,
            payment_status__code = 'NP',
            deposit_percentage = 30
        )
        reservation.save()

        return reservation


@login_required
def delete_reservation(request, reservation_id):
    room = Reservation.objects.get(id=reservation_id)
    room.delete()

    return redirect('reservations:list')


@method_decorator(login_required, name='dispatch')
class DetailsReservationView(View):
    template_name = 'reservations/admin/details.html'

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            reservation_id = kwargs.get('id')

        elif 'reservation' in request.GET:
            try:
                signed_data = request.GET.get('reservation')
                reservation_id = signing.loads(signed_data)

            except signing.BadSignature: raise Http404('Invalid Reservation ID')

        else:
            raise Http404("Reservation ID not provided")

        reservation: Reservation = get_object_or_404(Reservation, id=reservation_id)
        return render(request, self.template_name, { 'reservation': reservation })


    def post(self, request, *args, **kwargs):
        reservation_id = request.POST.get('reservation_id')
        reservation = get_object_or_404(Reservation, id=reservation_id)

        reservation.update_payment_status('FP')

        return render(request, self.template_name, { 'reservation': reservation })


