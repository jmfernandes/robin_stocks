import itertools
from datetime import datetime
from two_factor_log_in import *
from robin_stocks import robinhood as r
from robin_stocks.robinhood.options import (updateOptionsMarketData)
from calendar_spread import *

def find_calendar_spreads(symbol="SPY"):
    calendars = []
    # Get the list of options available and sort by strike_price and expiration_date
    options = r.options.find_tradable_options(
        symbol, optionType='call', info=None)

    options = updateOptionsMarketData(options)

    # # Create a create new calendar spread for every combination of expiration dates where the short front leg expiration_date is less than the long back leg of the spread
    sorted_options = sorted(options, key=lambda x: (
         float(x['strike_price']), datetime.strptime(x["expiration_date"], '%Y-%m-%d')))

    options_grouped_by_strike = itertools.groupby(
        sorted_options, lambda x: x['strike_price'])
    

    for (strike, option_items) in options_grouped_by_strike:
        for front_leg, back_leg in itertools.combinations(option_items, 2):
            if (datetime.strptime(front_leg["expiration_date"], '%Y-%m-%d') < datetime.strptime(back_leg["expiration_date"], '%Y-%m-%d')):
                print(strike,
                      front_leg['type'],
                      front_leg['expiration_date'],
                      back_leg['type'],
                      back_leg['expiration_date'])

                calendars.append(CalendarSpread(front_leg, back_leg))
    return calendars

def place_calendars_spreads(calendar):
    (front_leg, back_leg) = calendar

    params = [
            {
                'expirationDate': front_leg['expiration_date'],
                'strike': front_leg['strike_price'],
                'optionType': "call",
                'quantity': '1',
                'effect': 'open',
                'action': 'sell',
            },
            {
                'expirationDate': back_leg['expiration_date'],
                'strike': back_leg['strike_price'],
                'optionType': "call",
                'quantity': '1',
                'effect': 'open',
                'action': 'buy',
            },
        ]
    print(front_leg["type"], front_leg["strike_price"],
          front_leg["expiration_date"], back_leg["expiration_date"])

    return r.orders.order_option_spread(direction='debit', price='0.0', symbol=symbol, quantity='1', spread=params, timeInForce='gfd')


def get_top_twelve_calendar_spreads(calendar_spreads):

    filtered_calendar_spreads = list(
        filter(lambda x: x.is_placeable() > 0, calendar_spreads))

    for calendar_spread in filtered_calendar_spreads:
        spread = calendar_spread.get_leg_spread()
        print(spread)

    sorted_list = sorted(
        filtered_calendar_spreads, key=lambda x: x.get_leg_spread(), reverse=True)
    return sorted_list[:12]


def cancel_pending_options():
    # Get all pending orders
    pending_orders = r.orders.get_all_open_option_orders()

    # Loop through orders and cancel each one
    for order in pending_orders:
        print(r.cancel_option_order(order["id"]))

# Create a script that places a debit calendar spread for each tradeable option of a given symbol. The cost of the spread needs to be zero.
symbols = ["ET"]
loginmfa()

# For each stock
for symbol in symbols:
    calendar_spreads = find_calendar_spreads(symbol)

    top_twelve_trade_calendar_spreads = get_top_twelve_calendar_spreads(
        calendar_spreads)

    for calendar_spread in top_twelve_trade_calendar_spreads:
        # results = place_calendars_spreads(calendar)
        calendar_spread.print()


