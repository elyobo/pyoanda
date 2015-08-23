try:
    import unittest2 as unittest
except ImportError:
    import unittest
try:
    from unittest import mock
except ImportError:
    import mock

import types
from socket import error as SocketError

import requests_mock

from pyoanda.client import Client


class TestInstrumentsAPI(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            self.client = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )

    def test_get_instruments_pass(self):
        with mock.patch.object(
            Client, '_Client__call',
            return_value={"message": "good one"}
        ):
            assert self.client.get_instruments()

    def test_get_prices(self):
        with mock.patch.object(
            Client, '_Client__call',
            return_value={"message": "good one"}
        ):
            assert self.client.get_prices(instruments="EUR_GBP", stream=False)

    def test_get_instrument_history(self):
        with mock.patch.object(
            Client, '_Client__call',
            return_value=[{}]
        ):
            assert self.client.get_instrument_history('EUR_GBP')

class StreamResponse(object):
    def __init__(self, lines):
        self._lines = lines
        self.closed = False

    def read(self, blocks):
        try:
            return next(self._lines)
        except BaseException:
            self.closed = True
            raise


class TestPriceStreaming(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            self.client = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )

    @requests_mock.Mocker()
    def test_socket_timeout_reconnects(self, m):
        """Tests that streamed prices handle connection errors."""
        response_list = [
            'asdf\n',
            SocketError(104, 'Connection reset by peer'),
            'asdf\n',
        ]

        def respond():
            while response_list:
                item = response_list.pop(0)
                if isinstance(item, BaseException):
                    raise item
                yield item

        m.get(
            requests_mock.ANY,
            [
                {"body":StreamResponse(respond())},
                {"body":StreamResponse(respond())}
            ]
        );

        res = self.client.get_prices(instruments="EUR_GBP", stream=True)
        lines = [x for x in res.iter_lines()]
        self.assertEqual(lines, ['asdf', 'asdf'])
