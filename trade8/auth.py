import hmac
import hashlib
import time
import base64
from requests.auth import AuthBase


class T8Auth(AuthBase):
    # Provided by CBPro: https://docs.pro.coinbase.com/#signing-a-message
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def __call__(self, request):
        timestamp = str(round(time.time() * 1000))
        if 'trading' in request.path_url:
            path_url = request.path_url.split('trading')[1]
        else:
            path_url = request.path_url

        body = request.body.decode() if request.body else ''
        message = ''.join([timestamp, request.method, path_url, body])
        request.headers.update(get_auth_headers(timestamp, message,
                                                self.api_key,
                                                self.api_secret))
        return request


def get_auth_headers(timestamp, message, api_key, api_secret):
    signature = hmac.new(api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
    return {
        'WCX-APIKEY': api_key,
        'WCX-TIMESTAMP': timestamp,
        'WCX-SIG': signature_b64,
    }
