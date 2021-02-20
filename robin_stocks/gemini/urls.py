""" Module contains all the API endpoints """
from enum import Enum, auto
from re import IGNORECASE, match, split

from robin_stocks.gemini.helper import get_sandbox_flag


class AutoName(Enum):
    """Automatically sets an enum value to be its name when using auto()"""

    def _generate_next_value_(name, start, count, last_values):
        return name


class Version(AutoName):
    """Enum for different version types"""
    v1 = auto()
    v2 = auto()


class URLS:
    """ Static class for holding all urls."""
    __base_url = "https://api.gemini.com"
    __base_sandbox_url = "https://api.sandbox.gemini.com"

    def __init__(self):
        raise NotImplementedError(
            "Cannot create instance of {0}".format(self.__class__.__name__))

    @classmethod
    def get_base_url(cls, version):
        if get_sandbox_flag():
            url = cls.__base_sandbox_url
        else:
            url = cls.__base_url

        return url + "/" + version.value + "/"

    @classmethod
    def get_endpoint(cls, url):
        if match(cls.__base_sandbox_url, url, IGNORECASE):
            _, end = split(cls.__base_sandbox_url, url, IGNORECASE)
        elif match(cls.__base_url, url, IGNORECASE):
            _, end = split(cls.__base_url, url, IGNORECASE)
        else:
            raise ValueError("The URL has the wrong base.")
        
        return end

    # account.py
    @classmethod
    def account_detail(cls):
        return cls.get_base_url(Version.v1) + "account"

    @classmethod
    def available_balances(cls):
        return cls.get_base_url(Version.v1) + "balances"

    @classmethod
    def notional_balances(cls):
        return cls.get_base_url(Version.v1) + "notionalbalances/usd"

    @classmethod
    def transfers(cls):
        return cls.get_base_url(Version.v1) + "transfers"

    @classmethod
    def deposit_addresses(cls, network):
        return cls.get_base_url(Version.v1) + "addresses/{0}".format(network)

    @classmethod
    def approved_addresses(cls, network):
        return cls.get_base_url(Version.v1) + "approvedAddresses/account/{0}".format(network)

    @classmethod
    def withdrawl_crypto(cls, currency_code):
        return cls.get_base_url(Version.v1) + "withdraw/{0}".format(currency_code)

    # authentication.py
    @classmethod
    def heartbeat(cls):
        return cls.get_base_url(Version.v1) + "heartbeat"

    # crypto.py
    @classmethod
    def pubticker(cls, ticker):
        return cls.get_base_url(Version.v1) + "pubticker/{0}".format(ticker)

    @classmethod
    def ticker(cls, ticker):
        return cls.get_base_url(Version.v2) + "ticker/{0}".format(ticker)

    @classmethod
    def symbols(cls):
        return cls.get_base_url(Version.v1) + "symbols"

    @classmethod
    def symbol_details(cls, ticker):
        return cls.get_base_url(Version.v1) + "symbols/details/{0}".format(ticker)

    @classmethod
    def notional_volume(cls):
        return cls.get_base_url(Version.v1) + "notionalvolume"

    @classmethod
    def trade_volume(cls):
        return cls.get_base_url(Version.v1) + "tradevolume"

    # orders.py
    @classmethod
    def mytrades(cls):
        return cls.get_base_url(Version.v1) + "mytrades"

    @classmethod
    def cancel_session_orders(cls):
        return cls.get_base_url(Version.v1) + "order/cancel/session"

    @classmethod
    def cancel_order(cls):
        return cls.get_base_url(Version.v1) + "order/cancel"

    @classmethod
    def order_status(cls):
        return cls.get_base_url(Version.v1) + "order/status"

    @classmethod
    def active_orders(cls):
        return cls.get_base_url(Version.v1) + "orders"

    @classmethod
    def cancel_active_orders(cls):
        return cls.get_base_url(Version.v1) + "order/cancel/all"

    @classmethod
    def order_new(cls):
        return cls.get_base_url(Version.v1) + "order/new"
