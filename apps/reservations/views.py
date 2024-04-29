from urllib.parse import parse_qs
from django.shortcuts import render
from django.views import View
from django.contrib.admin.options import method_decorator
from django.contrib.auth.views import login_required
from django.contrib.sites.shortcuts import get_current_site
import django.http as http

from apps.webpay.views import WebpayAPI
from .models import Reservation

# TODO: Add session id
# TODO: Add reservation id
#@method_decorator(login_required, name='dispatch')
class RedirectPaymentView(View):
    template_name = 'reservations/checkout.html'

    def get(self, request):
        order_id = 'hotel-reef-order-123'
        order_total_amount = 400

        return_url = request.scheme + '://' + get_current_site(request).domain + '/result.html'
        session_id = 123# request.session.session_key

        webpay = WebpayAPI()
        response_data = webpay.create_transaction(order_total_amount, order_id, session_id, return_url)

        if response_data:
            url = response_data['url']
            token = response_data['token']

            return render(request, self.template_name, { 'url': url, 'token_ws': token, 'total_amount': order_total_amount })
        else:
            return http.JsonResponse({ 'message': 'Failed to create Webpay transaction' })


#@method_decorator(login_required, name='dispatch')
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
