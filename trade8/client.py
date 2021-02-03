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
        if auth:
            if self.auth:
                url = url + '?demo=true' if self.demo else url
                r = requests.request(method, url, params=params, auth=self.auth)
            else:
                print('authentication required!')  # todo: raise correct error
        else:
            # Use public endpoints, no authentication required and demo is irrelevant
            r = requests.request(method, url, params=params)

        return r

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

    def close_position(self, id):
        endpoint = '/trading/trade/close'
        params = {'id': id}
        return self._request('post', endpoint, params, auth=True)

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

    def get_products(self, product: str = ''):
        """
        List products available to trade
        :param product: (optional) Limits returned results to this product
        :return:
        """
        endpoint = f'/trading/products/{product}'
        return self._request('get', endpoint)

    def get_quotes(self, products: list):
        """
        Get quotes for the provided product(s)
        :param products: list of strings of one or more products
        :return:
        """
        endpoint = f"/trading/quotes/{','.join(products)}"
        return self._request('get', endpoint)

    def get_candles(self, product: str, resolution: str, **params):
        """
        Lists historical candles for a product. Candles returns are grouped by resolution.
        :param product: product to get candles for
        :param resolution: Time resolution for candle. Can be 1, 5, 15, 60, 240, or 1D.
        :param params: Optional named query parameters

        Optional query parameters:
            signal: string of 'mid', 'bid' or 'ask'. Defaults to 'mid'
            start: integer representing utc time in seconds after which to fetch candles
            end: integer representing utc time in seconds before which to fetch candles
            limit: string representing the number of candles to return, maximum is 150
        :return:
        """
        endpoint = f'/trading/candles/{product}/{resolution}'
        return self._request('get', endpoint, params)

