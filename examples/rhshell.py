#!/usr/bin/env python

import cmd
import datetime
import json
import logging
import math
import re
import sys
from pprint import pprint as pp

import yaml
from colorclass import Color
from tabulate import tabulate

import robin_stocks as rs
import robin_stocks.helper as helper

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('/tmp/{}.log'.format(datetime.date.today().isoformat()))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

"""
Base code/ideas from: https://github.com/anilshanbhag/RobinhoodShell
Thanks to @anilshanbhag

RHShell builds on Robinhood *unofficial* python library
to create a command line interface for interacting with Robinhood

* `l` : Lists your current portfolio's stocks
* `lo` : Lists your current portfolio's options
* `b <symbol> <quantity> <price>` : Submits a limit order to buy <quantity> stocks of <symbol> at <price>
* `s <symbol> <quantity> <price>` : Submits a limit order to sell <quantity> stocks of <symbol> at <price>
* `q <symbol>` : Get quote (current price) for symbol
* `q <symbol> <call/put> <strike_price> <(optional) expiration_date YYYY-mm-dd>` : Get quote for option, all expiration dates if none specified
* bto
* sto
* btc
* stc
* `o` : Lists all open orders
* `x` : list all open positions
* `c <id>` : Cancel an open order identified by <id> [<id> of a open order can be got from output of `o`]
* `bye` : Exit the shell
"""


class Helper:

    def __init__(self, rs):
        self.rs = rs
        self.rs.holdings = []
        self.rs.options = []

    def print_stock_positions(self):
        out = self.rs.get_current_positions()
        headers = ['No.', 'symbol', 'tradable_qty', 'current_price', 'average_price', 'quantity']
        holdings = []
        total = 0.0
        for idx, each in enumerate(out):
            each_instrument = each.get('instrument').split('/')[-2]
            stk_dict = self.rs.get_stock_quote_by_id(each_instrument)
            cur_price = stk_dict.get('last_extended_hours_trade_price') or stk_dict.get('last_trade_price')
            holdings.append([idx + 1,
                             stk_dict.get('symbol'),
                             float(each.get('quantity')) - sum(
                                 [float(each[x]) for x in each.keys() if 'shares_held' in x]),
                             cur_price,
                             each.get('average_buy_price'),
                             each.get('quantity'),
                             ])
            total += float(cur_price) * float(each.get('quantity'))
        self.rs.holdings = holdings
        if holdings:
            print(tabulate(holdings, headers=headers))
            print("*** Net Equity: {}".format(total))
        else:
            print("**** No stock holdings")

    def get_open_options(self):
        positions = []
        for each_pos in rs.get_open_option_positions():
            if each_pos['quantity'] != "0.0000":
                url = each_pos['option']
                data = helper.request_get(url)
                mkt_data = self.rs.get_option_market_data_by_id(url.split('/')[-2])
                # fill out the data
                each_pos['optype'] = data['type']
                each_pos['expiration_date'] = data['expiration_date']
                each_pos['created_at'] = data['created_at']
                each_pos['strike_price'] = data['strike_price']
                price_tag = 'ask_price' if each_pos['type'] is 'short' else 'bid_price'
                qty_tag = 'pending_buy_quantity' if each_pos['type'] is 'short' else 'pending_sell_quantity'
                each_pos['curr_price'] = mkt_data[price_tag]
                each_pos['tradable_qty'] = float(each_pos['quantity']) - float(each_pos[qty_tag])
                #    sum([float(each_pos[x]) for x in each_pos.keys() if 'pending_' in x])
                positions.append(each_pos)
        return positions

    def print_open_options(self):
        headers = ["No.", "Symbol", "strike", "expiry", "C/P", "curr", "Qty", "avg"]
        positions = self.get_open_options()
        positions.sort(key=lambda x: (x['chain_symbol'], x['optype'], x['type'], x['average_price']))
        table = []
        total = 0.0
        for idx, each in enumerate(positions):
            table.append(["#{}".format(idx + 1),
                          each['chain_symbol'],
                          each['strike_price'],
                          each['expiration_date'],
                          each['optype'],
                          each['curr_price'],
                          "{}/{}".format(int(each['tradable_qty']) * (-1 if each['type'] == "short" else 1),
                                         int(float(each['quantity']))),
                          math.ceil(float(each['average_price'])) / 100,
                          ])
            total += float(each['quantity']) * float(each['curr_price']) * 100
        self.rs.options = table
        if table:
            print(tabulate(table, headers=headers))
            print("Net Equity: {}".format(int(total)))
        else:
            print("*** No option positions")

    def merge_spread(self, *args):
        headers = ["No.", "Symbol", "C/P", "strike", "expiry", "St/Lg", "Qty", "avg", "curr"]
        table = []
        for each in args:
            table.append(self.rs.options[int(each) - 1])
        if table:
            print(tabulate(table, headers=headers))
        else:
            print("*** No option positions")


# END OF HELPER CODE


class RHShell(cmd.Cmd):
    intro = 'Welcome to the shell. Type help or ? to list commands.\n'
    prompt = '> '

    # API Object
    trader = None

    # Cache file used to store instrument cache
    instruments_cache_file = 'instruments.data'

    # Maps Symbol to Instrument URL
    instruments_cache = {}

    # Maps URL to Symbol
    instruments_reverse_cache = {}

    # Cache file used to store instrument cache
    watchlist_file = 'watchlist.data'

    # List of stocks in watchlist
    watchlist = []

    def __init__(self, yaml_file):
        cmd.Cmd.__init__(self)
        self.trader = rs
        with open(yaml_file) as fh:
            yd = yaml.safe_load(fh)
        rs.login(yd['username'], yd['password'], pickle_path=yd.get('pickle_path', "data.pickle"))
        self.prompt = "{}> ".format(yd['username'][:2])
        print("Logging in..")
        self.h = Helper(self.trader)

    def do_l(self, arg):
        """
        Lists current portfolio

        """
        self.h.print_stock_positions()

    def do_lo(self, arg):
        """
        Lists current options portfolio

        """
        self.h.print_open_options()

    def do_w(self, arg):
        """
        Show watchlist w
        Add to watchlist w a <symbol>
        Remove from watchlist w r <symbol>
        ** WIP **
        """
        pass

    def do_b(self, arg):
        """
        Buy stock b <symbol> <quantity> <price> # LIMIT order
        Buy stock b <symbol> <quantity>  # MARKET order
        """
        od = self._construct_stock_dict(arg)
        if od['limit_price']:
            self.trader.order_buy_limit(**od)
        else:
            self.trader.order_buy_market(**od)

    def do_s(self, arg):
        """
        Sell stock s <symbol> <quantity> <?price> # LIMIT order
        Sell stock s <symbol> <quantity> # MARKET order
        """
        od = self._construct_stock_dict(arg)
        if od['limit_price']:
            self.trader.order_sell_limit(**od)
        else:
            self.trader.order_sell_market(**od)

    def do_slb(self, arg):
        """
        Setup stop loss buy on stock slb <symbol> <quantity> <stoploss> <~ price>
        """
        od = self._construct_sl_stock_dict(arg)
        if od['limit_price']:
            self.trader.order_buy_stop_limit(**od)
        else:
            self.trader.order_buy_stop_loss(**od)

    def do_sls(self, arg):
        """
        Setup stop loss sell on stock slb <symbol> <quantity> <stoploss> <~ price>
        """
        od = self._construct_sl_stock_dict(arg)
        if od['limit_price']:
            self.trader.order_sell_stop_limit(**od)
        else:
            self.trader.order_sell_stop_loss(**od)

    def do_tslb(self, arg):
        """
        ** WIP **
        Setup trail stop loss buy on stock slb <symbol> <quantity> <stoploss> <~ price>
        """
        od = self._construct_sl_stock_dict(arg)
        if od['limit_price']:
            self.trader.order_buy_stop_limit(**od)
        else:
            self.trader.order_buy_stop_loss(**od)

    def do_tsls(self, arg):
        """
        ** WIP **
        Setup trail stop loss sell on stock slb <symbol> <quantity> <stoploss> <~ price>
        """
        od = self._construct_sl_stock_dict(arg)
        if od['limit_price']:
            self.trader.order_sell_stop_limit(**od)
        else:
            self.trader.order_sell_stop_loss(**od)

    def do_o(self, arg):
        """
        List open orders
        """
        open_orders = self.trader.get_all_open_orders()
        pp(open_orders)

    def do_op(self, arg):
        """
        
        :param arg: 
        :return: 
        """
        open_orders = self.trader.get_all_open_option_orders()
        pp(open_orders)

    def do_c(self, arg):
        """
        Cancel open order c <index> or c <id>
        where <index> is cached list of open orders
        (or)
        <id> actual robinhood ID of the order
        """
        if len(arg) < 8:
            _id = self.open_orders[int(arg)].get('id')
        else:
            _id = arg
        self.trader.cancel_order(order_id=_id)

    def do_co(self, arg):
        """
        
        :param arg: 
        :return: 
        """
        self.trader.cancel_all_open_option_orders()

    def do_ca(self, arg):
        """
        cancel all open orders
        """
        self.trader.cancel_all_open_orders()

    def do_m(self, arg):
        """

        """
        args = re.split(r"\W+", arg)
        self.h.merge_spread(*args)

    def do_q(self, arg):
        """
        Get detailed quote for stock: q <symbol(s)>
        """
        symbols = re.split('\W+', arg)
        out = self.trader.get_quotes(symbols)
        pp(out)

    def do_oq(self, arg):
        """
        Get quote for oq <symbol> <expiration_date> <strike> <call/put>
        """
        symbol, expiration_date, strike, option_type = arg.strip().split()
        out = self.trader.get_option_market_data(symbol, expiration_date, strike, option_type)
        pp(out)

    def do_e(self, arg):
        """
        call bye
        """
        self.do_bye(arg)

    def do_bto(self, arg):
        """
        symbol, strike, expdate, opttype, price, qty

        """
        od = self._construct_option_dict(arg)
        self.trader.order_buy_option_limit(**od)

    def do_stc(self, arg):
        """
        symbol, strike, expdate, opttype, price, qty

        """
        od = self._construct_option_dict(arg)
        self.trader.order_option_sell_to_close(**od)

    def do_sto(self, arg):
        """

        """
        od = self._construct_option_dict(arg)
        self.trader.order_option_sell_to_open(**od)

    @staticmethod
    def _construct_stock_dict(arg):
        symbol, quantity, limit_price, time_in_force, extended_hours = (arg.strip().split() + [None] * 3)[:5]
        od = dict()
        od['symbol'] = symbol
        od['quantity'] = quantity
        if limit_price:
            od['limit_price'] = limit_price
        od['time_in_force'] = time_in_force or 'gtc'
        # od['extended_hours'] = extended_hours or 'false'
        pp(od)
        return od

    @staticmethod
    def _construct_sl_stock_dict(arg):
        """
        construct stop loss order
        """
        symbol, quantity, stop_price, limit_price, time_in_force, extended_hours = (arg.strip().split() + [None] * 3)[
                                                                                   :6]
        od = dict()
        od['symbol'] = symbol
        od['quantity'] = quantity
        od['stop_price'] = stop_price
        if limit_price:
            od['limit_price'] = limit_price
        od['time_in_force'] = time_in_force or 'gtc'
        # od['extended_hours'] = extended_hours or 'false'
        pp(od)
        return od

    @staticmethod
    def _construct_option_dict(arg):
        symbol, strike, expdate, opttype, price, qty = arg.strip().split()
        od = dict()
        od['price'] = price
        od['symbol'] = symbol
        od['expiration_date'] = str(expdate)
        od['quantity'] = qty
        od['strike'] = strike
        od['option_type'] = opttype
        pp(od)
        return od

    def do_btc(self, arg):
        """

        """
        od = self._construct_option_dict(arg)
        self.trader.order_option_buy_to_close(**od)

    def do_bye(self, arg):
        """
        exit the terminal
        """
        open(self.instruments_cache_file, 'w').write(json.dumps(self.instruments_cache))
        open(self.watchlist_file, 'w').write(json.dumps(self.watchlist))
        sys.exit(0)
        return True

    # ------ utils --------
    def get_symbol(self, url):
        if url not in self.instruments_reverse_cache:
            self.add_instrument_from_url(url)

        return self.instruments_reverse_cache[url]

    def get_instrument(self, symbol):
        if not symbol in self.instruments_cache:
            instruments = self.trader.instruments(symbol)
            for instrument in instruments:
                self.add_instrument(instrument['url'], instrument['symbol'])

        url = ''
        if symbol in self.instruments_cache:
            url = self.instruments_cache[symbol]

        return {'symbol': symbol, 'url': url}

    def add_instrument_from_url(self, url):
        data = self.trader.get_url(url)
        if 'symbol' in data:
            symbol = data['symbol']
        else:
            types = {'call': 'C', 'put': 'P'}
            symbol = data['chain_symbol'] + ' ' + data['expiration_date'] + ' ' + ''.join(
                types[data['type']].split('-')) + ' ' + str(float(data['strike_price']))
        self.add_instrument(url, symbol)

    def add_instrument(self, url, symbol):
        self.instruments_cache[symbol] = url
        self.instruments_reverse_cache[url] = symbol


def color_data(value):
    if float(value) > 0:
        number = Color('{autogreen}' + str(value) + '{/autogreen}')
    elif float(value) < 0:
        number = Color('{autored}' + str(value) + '{/autored}')
    else:
        number = str(value)

    return number


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))


if __name__ == '__main__':
    RHShell(sys.argv[1]).cmdloop()
