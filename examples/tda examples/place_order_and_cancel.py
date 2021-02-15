''' An example on how to place an order and then cancel it.
'''
import os

import robin_stocks.tda as tda
from dotenv import load_dotenv

load_dotenv()

# login
tda.login(os.environ["tda_encryption_passcode"])
# format the order payload
order = {
    "orderType": "MARKET",
    "session": "NORMAL",
    "duration": "DAY",
    "orderStrategyType": "SINGLE",
    "orderLegCollection": [
        {
            "instruction": "Buy",
            "quantity": 1,
            "instrument": {
                "symbol": "AMC",
                "assetType": "EQUITY"
            }
        }
    ]
}
data, err = tda.place_order(os.environ["tda_order_account"], order, True)
order_id = tda.get_order_number(data)
print("the order has been placed and the order id is ", order_id)
cancel, err = tda.cancel_order(os.environ["tda_order_account"], order_id, False)
print("the order has been cancelled")
print(cancel.headers)
