from .auth import T8Auth
import requests
from urllib.parse import urlencode


class Client:
    API_URL = 'https://api.trade8.to'

    def __init__(self, api_key=None, api_secret=None):

        self.auth = T8Auth(api_key, api_secret) if api_key and api_secret else None

    def _request(self, method, endpoint, params=None, auth=False):
        url = self.API_URL + endpoint
        if auth:
            if self.auth:
                r = requests.request(method, url, auth=self.auth)
            else:
                print('authentication required!')  # todo: handle exception
        else:
            r = requests.request(method, url, params=params)
            print(r.url)

        return r.json()

    def get_positions(self):
        endpoint = '/trading/positions'
        return self._request('get', endpoint, auth=True)

    def get_candles(self, product, resolution, **params):
        endpoint = f'/trading/candles/{product}/{resolution}'
        return self._request('get', endpoint, params)
