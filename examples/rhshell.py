#!/usr/bin/env python

import cmd
import datetime
import json
import logging
import re
import sys
from os import system, name
from pprint import pprint as pp

import yaml
from colorclass import Color

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

    @staticmethod
    def print_spread(spread):

        if (spread['enable']):
            if spread['print_empty_line']:
                print(
                    "                                                            ------------------------------------------")
            print("                                                           %10.2f            %10.2f %10.2f"
                  % (spread['aprice'], spread['cprice'], spread['p_or_l']))
            spread['aprice'] = 0.0
            spread['cprice'] = 0.0
            spread['p_or_l'] = 0.0

    @staticmethod
    def print_symbol(symbol):

        if (symbol['enable']):
            if symbol['print_empty_line']:
                print(
                    "                                                            ------------------------------------------")
            print("                                                                                            %10.2f"
                  % (symbol['p_or_l']))
            symbol['p_or_l'] = 0.0

    @staticmethod
    def print_summary(summary):

        if (summary['enable']):
            if summary['print_empty_line']:
                print(
                    "                                                            ------------------------------------------")
            print("                                                                                    Total   %10.2f"
                  % (summary['p_or_l']))

    @staticmethod
    def clear_screen():
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def get_mktdata_for_positions(self, posns):

        for position in posns:
            if position['quantity'] != "0.0000":
                url = position['option']
                urll = url.split("/")
                opt_id = urll[len(urll) - 2]
                mkt_data = self.rs.get_option_market_data_by_id(opt_id)
                position['curr_price'] = mkt_data['adjusted_mark_price']

        return posns

    def get_all_my_open_positions(self):

        # !!! Fill out username and password
        positions = rs.get_open_option_positions()
        posns = []

        for position in positions:

            if position['quantity'] != "0.0000":
                url = position['option']
                data = helper.request_get(url)
                optype = data['type']

                urll = url.split("/")
                opt_id = urll[len(urll) - 2]
                mkt_data = self.rs.get_option_market_data_by_id(opt_id)

                position['optype'] = optype
                position['expiration_date'] = data['expiration_date']
                position['created_at'] = data['created_at']
                position['strike_price'] = data['strike_price']
                position['curr_price'] = mkt_data['adjusted_mark_price']

                posns.append(position)

        return posns

    def print_positions(self, posns):

        # clear_screen()

        print("Symbol   C/P  Strike  expry  Enter    S/B   Qty      avg/s        avg     curr/s    current        p/l")
        print("------------------------------------------------------------------------------------------------------")

        p_symbol = None
        p_optype = ""
        p_ptype = ""
        spread = {}
        spread['enable'] = True
        spread['print_empty_line'] = False
        spread['aprice'] = 0.0
        spread['cprice'] = 0.0
        spread['p_or_l'] = 0.0

        symbol = {}
        symbol['enable'] = True
        symbol['print_empty_line'] = False
        symbol['sname'] = ""
        symbol['p_or_l'] = 0.0

        summary = {}
        summary['enable'] = True
        summary['print_empty_line'] = False
        summary['p_or_l'] = 0.0

        for position in posns:
            sname = position['chain_symbol'].strip()
            optype = position['optype'].strip()
            ptype = position['type'].strip()

            if p_symbol is not None:
                if p_symbol != sname or p_optype != optype:
                    self.print_spread(spread)

                    if p_symbol != sname:
                        self.print_symbol(symbol)
                        symbol['sname'] = sname
                    print()

            qty = int(float(position['quantity']))
            aprice = float(position['average_price'])
            sprice = float(position['strike_price'])
            cprice = float(position['curr_price'])

            edate = position['expiration_date'][-5:]
            cdate = position['created_at'][5:10]

            spread['aprice'] += (aprice * qty)
            cprice = cprice * 100

            if (ptype == "short"):
                p_or_l = (-1 * aprice * qty) - (cprice * qty)
            else:
                p_or_l = cprice * qty - aprice * qty

            spread['cprice'] += (cprice * qty)
            spread['p_or_l'] += p_or_l
            symbol['p_or_l'] += p_or_l
            summary['p_or_l'] += p_or_l

            print(" %5s %5s %7s %6s %6s %6s %5d %10.2f %10.2f %10.2f %10.2f %10.2f"
                  % (
                      sname, optype, sprice, edate, cdate, ptype, qty, aprice, aprice * qty, cprice, cprice * qty,
                      p_or_l))

            p_symbol = sname
            p_optype = optype
            p_ptype = ptype

        self.print_spread(spread)
        self.print_symbol(symbol)
        self.print_summary(summary)

    def print_all_positions(self):

        posns = self.get_all_my_open_positions()
        posns.sort(key=lambda x: (x['chain_symbol'], x['optype'], x['type'], x['average_price']))
        self.print_positions(posns)

        posns = self.get_mktdata_for_positions(posns)
        self.print_positions(posns)


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
        print("Logging in..")

    def do_x(self, arg):
        """

        """
        Helper(self.trader).print_all_positions()

    def do_l(self, arg):
        """
        Lists current portfolio

        """
        open_positions = self.trader.get_all_positions()
        pp(open_positions)

    def do_lo(self, arg):
        """
        Lists current options portfolio

        """
        # Load Options
        option_positions = self.trader.get_open_option_positions()
        pp(option_positions)

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
        open_orders = self.trader.get_open_orders()
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

    def do_ca(self, arg):
        """
        cancel all open orders
        """
        self.trader.cancel_all_open_orders()

    def do_mp(self, arg):
        """

        """
        pass

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

        """
        od = self._construct_option_dict(arg)
        self.trader.order_buy_option_limit(**od)

    def do_stc(self, arg):
        """

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
