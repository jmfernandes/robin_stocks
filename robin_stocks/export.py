import csv
import datetime as dt
import robin_stocks.helper as helper
import robin_stocks.orders as orders
import robin_stocks.stocks as stocks


@helper.login_required
def export_completed_stock_orders(file_path):
    """Write all completed orders to a csv file
    
    :param file_path: absolute path to the location the file will be written.
    :type file_path: str

    """
    all_orders = orders.get_all_orders()
    with open(f"{file_path}stock_orders_{dt.date.today().strftime('%b-%d-%Y')}.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'symbol',
            'date',
            'order_type', 
            'side',
            'fees',
            'quantity',
            'average_price'
        ])
        for order in all_orders:
            if order['state'] == 'filled' and order['cancel'] is None:
                writer.writerow([
                    stocks.get_symbol_by_url(order['instrument']),
                    order['last_transaction_at'],
                    order['type'],
                    order['side'],
                    order['fees'],
                    order['quantity'],
                    order['average_price']
                ])
        f.close()

@helper.login_required
def export_completed_option_orders(file_path):
    """Write all completed option orders to a csv
        
        :param file_path: absolute path to the location the file will be written.
        :type file_path: str

    """
    all_orders = orders.get_all_option_orders()
    with open(f"{file_path}option_orders_{dt.date.today().strftime('%b-%d-%Y')}.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
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
                    instrument_data = helper.request_get(leg['option'])
                    writer.writerow([
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