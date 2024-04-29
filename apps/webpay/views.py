import http.client
import json
import logging

from .conf import settings

class WebpayAPI:
    def create_transaction(self, amount, order_id, session_id, return_url):
        conn = http.client.HTTPSConnection(host=settings.WEBPAY_HOST)
        endpoint = settings.WEBPAY_API_URL + '/transactions'

        data = {
            'buy_order': order_id,
            'session_id': session_id,
            'amount': amount,
            'return_url': return_url,
        }

        try:
            conn.request('POST', endpoint, json.dumps(data), headers=self.headers)
            response = conn.getresponse()

            if response.status == 200 and response.headers['Content-Type'] == 'application/json':
                return json.loads(response.read().decode('utf-8'))
            else:
                logging.info(f'INFO: [webpay] Create transaction response code: [{response.status}]')
                return None

        except Exception as e:
            logging.error(f'ERROR: [webpay] making API request: {e}')
            return None


    def commit_transaction(self, token):
        conn = http.client.HTTPSConnection(host=settings.WEBPAY_HOST)
        endpoint = settings.WEBPAY_API_URL + f'/transactions/{token}'

        try:
            conn.request('PUT', endpoint, headers=self.headers)
            response = conn.getresponse()

            if response.status == 200 and response.headers['Content-Type'] == 'application/json':
                return json.loads(response.read().decode('utf-8'))
            else:
                logging.info(f'INFO: [webpay] Commit transaction response code: [{response.status}]')
                return None

        except Exception as e:
            logging.error(f'ERROR: [webpay] making API request: {e}')
            return None


    @property
    def headers(self):
        return {
            'Tbk-Api-Key-Id': settings.WEBPAY_COMMERCE_CODE,
            'Tbk-Api-Key-Secret': settings.WEBPAY_SECRET_KEY,
            'Content-Type': 'application/json',
        }
