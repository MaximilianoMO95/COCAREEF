import os

class Settings:
    WEBPAY_INTEGRATION_TYPE = os.getenv('WEBPAY_INTEGRATION_TYPE', 'TEST')

    WEBPAY_HOST = 'webpay3gint.transbank.cl'
    WEBPAY_API_URL = 'https://' + WEBPAY_HOST + '/rswebpaytransaction/api/webpay/v1.2'

    WEBPAY_SECRET_KEY = os.getenv('WEBPAY_SECRET_KEY', '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C')
    WEBPAY_COMMERCE_CODE = os.getenv('WEBPAY_COMMERCE_CODE', '597055555532')

    def __init__(self):
        if self.WEBPAY_INTEGRATION_TYPE != 'TEST':
            self.WEBPAY_HOST = 'webpay3g.transbank.cl'

        if not self.WEBPAY_SECRET_KEY or not self.WEBPAY_COMMERCE_CODE:
            raise ValueError('WEBPAY_SECRET_KEY and WEBPAY_COMMERCE_CODE must be defined in your .env file.')

settings = Settings()
