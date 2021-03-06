from .client import Client
from .order import Order

__version__ = "0.9"


# OANDA API URLS
SANDBOX = (
    "http://api-sandbox.oanda.com",
    "http://stream-sandbox.oanda.com"
)
PRACTICE = (
    "https://api-fxpractice.oanda.com",
    "https://stream-fxpractice.oanda.com"
)
TRADE = (
    "https://api-fxtrade.oanda.com",
    "https://stream-fxtrade.oanda.com"
)
