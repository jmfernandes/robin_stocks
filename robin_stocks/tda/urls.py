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
    __base_url = "https://api.tdameritrade.com"

    def __init__(self):
        raise NotImplementedError(
            "Cannot create instance of {0}".format(self.__class__.__name__))

    @classmethod
    def get_base_url(cls, version):
        return cls.__base_url + "/" + version.value + "/"

    @classmethod
    def get_endpoint(cls, url):
        if match(cls.__base_url, url, IGNORECASE):
            _, end = split(cls.__base_url, url, IGNORECASE)
        else:
            raise ValueError("The URL has the wrong base.")

        return end

    # accounts.py
    @classmethod
    def account(cls, id):
        return cls.get_base_url(Version.v1) + "accounts/{0}".format(id)

    @classmethod
    def accounts(cls):
        return cls.get_base_url(Version.v1) + "accounts"

    @classmethod
    def transaction(cls, id, transaction):
        return cls.get_base_url(Version.v1) + "accounts/{0}/transactions/{1}".format(id, transaction)

    @classmethod
    def transactions(cls, id):
        return cls.get_base_url(Version.v1) + "accounts/{0}/transactions".format(id)

    # authentication.py
    @classmethod
    def oauth(cls):
        return cls.get_base_url(Version.v1) + "oauth2/token"

    # markets.py
    @classmethod
    def markets(cls):
        return cls.get_base_url(Version.v1) + "marketdata/hours"

    @classmethod
    def market(cls, market):
        return cls.get_base_url(Version.v1) + "marketdata/{0}/hours".format(market)

    @classmethod
    def movers(cls, index):
        return cls.get_base_url(Version.v1) + "marketdata/{0}/movers".format(index)

    # orders.py
    @classmethod
    def orders(cls, account_id):
        return cls.get_base_url(Version.v1) + "accounts/{0}/orders".format(account_id)

    @classmethod
    def order(cls, account_id, order_id):
        return cls.get_base_url(Version.v1) + "accounts/{0}/orders/{1}".format(account_id, order_id)

    # stocks.py
    @classmethod
    def instruments(cls):
        return cls.get_base_url(Version.v1) + "instruments"

    @classmethod
    def instrument(cls, cusip):
        return cls.get_base_url(Version.v1) + "instruments/{0}".format(cusip)

    @classmethod
    def quote(cls, ticker):
        return cls.get_base_url(Version.v1) + "marketdata/{0}/quotes".format(ticker)

    @classmethod
    def quotes(cls):
        return cls.get_base_url(Version.v1) + "marketdata/quotes"

    @classmethod
    def price_history(cls, ticker):
        return cls.get_base_url(Version.v1) + "marketdata/{0}/pricehistory".format(ticker)

    @classmethod
    def option_chains(cls):
        return cls.get_base_url(Version.v1) + "marketdata/chains"
