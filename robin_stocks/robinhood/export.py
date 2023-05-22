from csv import writer
from datetime import date
from pathlib import Path
from robin_stocks.robinhood.helper import *
from robin_stocks.robinhood.orders import *
from robin_stocks.robinhood.stocks import *
from robin_stocks.robinhood.crypto import *


def fix_file_extension(file_name):
    """ Takes a file extension and makes it end with .csv

    :param file_name: Name of the file.
    :type file_name: str
    :returns: Adds or replaces the file suffix with .csv and returns it as a string.

    """
    path = Path(file_name)
    path = path.with_suffix('.csv')
    return path.resolve()

def create_absolute_csv(dir_path, file_name, order_type):
    """ Creates a filepath given a directory and file name.

    :param dir_path: Absolute or relative path to the directory the file will be written.
    :type dir_path: str
    :param file_name: An optional argument for the name of the file. If not defined, filename will be stock_orders_{current date}
    :type file_name: str
    :param file_name: Will be 'stock', 'option', or 'crypto'
    :type file_name: str
    :returns: An absolute file path as a string.

    """
    path = Path(dir_path)
    directory = path.resolve()
    if not file_name:
        file_name = "{}_orders_{}.csv".format(order_type, date.today().strftime('%b-%d-%Y'))
    else:
        file_name = fix_file_extension(file_name)
    return(Path.joinpath(directory, file_name))


@login_required
def export_completed_stock_orders(dir_path, file_name=None):
    """Write all completed orders to a csv file

    :param dir_path: Absolute or relative path to the directory the file will be written.
    :type dir_path: str
    :param file_name: An optional argument for the name of the file. If not defined, filename will be stock_orders_{current date}
    :type file_name: Optional[str]

    """
    file_path = create_absolute_csv(dir_path, file_name, 'stock')
    all_orders = get_all_stock_orders()
    with open(file_path, 'w', newline='') as f:
        csv_writer = writer(f)
        csv_writer.writerow([
            'symbol',
            'date',
            'order_type',
            'side',
            'fees',
            'quantity',
            'average_price'
        ])
        for order in all_orders:
            # include candled order if partial executed
            if order['state'] == 'cancelled' and len(order['executions']) > 0:
                for partial in order['executions']:
                    csv_writer.writerow([
                        get_symbol_by_url(order['instrument']),
                        partial['timestamp'],
                        order['type'],
                        order['side'],
                        order['fees'],
                        partial['quantity'],
                        partial['price']
                    ])

            if order['state'] == 'filled' and order['cancel'] is None:
                csv_writer.writerow([
                    get_symbol_by_url(order['instrument']),
                    order['last_transaction_at'],
                    order['type'],
                    order['side'],
                    order['fees'],
                    order['quantity'],
                    order['average_price']
                ])
        f.close()
    
@login_required
def export_completed_crypto_orders(dir_path, file_name=None):
    """Write all completed crypto orders to a csv file

    :param dir_path: Absolute or relative path to the directory the file will be written.
    :type dir_path: str
    :param file_name: An optional argument for the name of the file. If not defined, filename will be crypto_orders_{current date}
    :type file_name: Optional[str]

    """
    file_path = create_absolute_csv(dir_path, file_name, 'crypto')
    all_orders = get_all_crypto_orders()
    
    with open(file_path, 'w', newline='') as f:
        csv_writer = writer(f)
        csv_writer.writerow([
            'symbol',
            'date',
            'order_type',
            'side',
            'fees',
            'quantity',
            'average_price'
        ])
        for order in all_orders:
            if order['state'] == 'filled' and order['cancel_url'] is None:
                try:
                    fees = order['fees']
                except KeyError:
                    fees = 0.0
                csv_writer.writerow([
                    get_crypto_quote_from_id(order['currency_pair_id'], 'symbol'),
                    order['last_transaction_at'],
                    order['type'],
                    order['side'],
                    fees,
                    order['quantity'],
                    order['average_price']
                ])
        f.close()


@login_required
def export_completed_option_orders(dir_path, file_name=None):
    """Write all completed option orders to a csv

        :param dir_path: Absolute or relative path to the directory the file will be written.
        :type dir_path: str
        :param file_name: An optional argument for the name of the file. If not defined, filename will be option_orders_{current date}
        :type file_name: Optional[str]

    """
    file_path = create_absolute_csv(dir_path, file_name, 'option')
    all_orders = get_all_option_orders()
    with open(file_path, 'w', newline='') as f:
        csv_writer = writer(f)
        csv_writer.writerow([
            'chain_symbol',
            'expiration_date',
            'strike_price',
            'option_type',
            'side',
            'order_created_at',
            'direction',
            'order_quantity',
            'order_type',
            'opening_strategy',
            'closing_strategy',
            'price',
            'processed_quantity'
        ])
        for order in all_orders:
            if order['state'] == 'filled':
                for leg in order['legs']:
                    instrument_data = request_get(leg['option'])
                    csv_writer.writerow([
                        order['chain_symbol'],
                        instrument_data['expiration_date'],
                        instrument_data['strike_price'],
                        instrument_data['type'],
                        leg['side'],
                        order['created_at'],
                        order['direction'],
                        order['quantity'],
                        order['type'],
                        order['opening_strategy'],
                        order['closing_strategy'],
                        order['price'],
                        order['processed_quantity']
                    ])
        f.close()
