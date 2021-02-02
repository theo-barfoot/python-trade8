from .auth import T8Auth
import requests
from urllib.parse import urlencode


class Client:
    API_URL = 'https://api.trade8.to'

    def __init__(self, api_key=None, api_secret=None, demo=True):

        self.auth = T8Auth(api_key, api_secret) if api_key and api_secret else None
        self.demo = demo

    def _request(self, method, endpoint, params=None, auth=False):
        url = self.API_URL + endpoint
        url = url + '?demo=true' if self.demo else url
        if auth:
            if self.auth:
                r = requests.request(method, url, auth=self.auth)
            else:
                print('authentication required!')  # todo: raise correct error
        else:
            r = requests.request(method, url, params=params)
            print(r.url)

        return r.json()

    def get_positions(self):
        endpoint = '/trading/positions'
        return self._request('get', endpoint, auth=True)

    def cancel_order(self, id: str):
        """

        :param id: The ID of the order to cancel
        :return: ID of order cancelled or an error
        """
        endpoint = '/trading/trade/cancel'
        pass

    def update_order(self):
        pass

    def close_position(self):
        pass

    def split_position(self):
        pass

    def get_orders(self):
        pass

    def get_orders(self):
        pass

    def get_history(self):
        pass

    def get_balances(self):
        pass

    def get_transactions(self):
        pass

    def get_deposit_address(self):
        pass

    # Public endpoints:

    def get_products(self):
        pass

    def get_quotes(self):
        pass

    def get_candles(self, product, resolution, **params):
        endpoint = f'/trading/candles/{product}/{resolution}'
        return self._request('get', endpoint, params)

