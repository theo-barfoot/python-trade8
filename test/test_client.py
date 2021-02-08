import unittest
from trade8 import Client
import os

# API_KEY = os.environ['API_KEY']
# API_SECRET = os.environ['API_SECRET']

# Test public endpoints:


class GetProducts(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.product = 'XAU-USD'

    def test_get_products(self):
        """ Test that get products function returns a dictionary of length greater than zero"""
        r = self.client.get_products()
        self.assertIsInstance(r, dict)
        self.assertGreater(len(r), 0)

    def test_get_specific_product(self):
        """ Test that get products function return specified product"""
        r = self.client.get_products(self.product)
        self.assertEqual(self.product, r['product'])


class GetQuotes(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.product = ['XAG-USD']
        self.products = ['XAG-USD', 'EUR-USD', 'AAPL']

    def test_get_one_quote(self):
        """ Test that get quotes function returns one quote as specified"""
        r = self.client.get_quotes(self.product)
        self.assertEqual(1, len(r))
        self.assertEqual(self.product, list(r.keys()))

    def test_get_quotes(self):
        """Test that get quotes function returns multiple quotes as specified"""
        r = self.client.get_quotes(self.products)
        self.assertGreater(len(r), 1)


class GetCandles(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_get_candles(self):
        """Test the get candles function returns candles"""
        r = self.client.get_candles('XRP-USD', 60)
        self.assertIsInstance(r, list)
        self.assertTrue(r)

    def test_candle_resolution(self):
        """Test that candles with 1 minute resolution are in fact 60 seconds in resolution"""
        r = self.client.get_candles('XRP-USD', 1)
        interval = int(r[0][0]) - int(r[1][0])
        self.assertEqual(interval, 60)

    def test_candle_limit(self):
        """ Test that limiting candles to specific amount works"""
        r = self.client.get_candles('AMZN', 240, limit=10)
        self.assertEqual(10, len(r))

    def test_candle_start_stop(self):
        """ Test that requesting candles from a specific start time works
        The time has to be specified in multiples of 60, given that the minimum candle is 60s (1 minute)"""
        t = int(self.client.get_candles('BTC-USD', 1)[0][0])  # get latest time stamp
        start = t - 1000*60  # set start time as 1000 minutes before this
        end = start + 30*60  # set end time 30 minutes after this
        r = self.client.get_candles('BTC-USD', 1, start=start, end=end)
        self.assertEqual(start, int(r[-1][0]))
        self.assertEqual(end, int(r[0][0]))
        self.assertEqual(31, len(r))

    def test_candle_signal(self):
        """ Test that signal can be specified """
        self.client.get_candles('BTC-USD', 1, signal='mid')
