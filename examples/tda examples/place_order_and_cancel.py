''' An example on how to place an order and then cancel it.
'''
import os

import robin_stocks.tda as tda
from dotenv import load_dotenv

load_dotenv()

# login
tda.login(encryption_passcode=os.environ["tda_encryption_passcode"])
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
data, err = tda.place_order(account_id=os.environ["tda_order_account"], order_payload=order, jsonify=True)
order_id = tda.get_order_number(data=data)
print("the order has been placed and the order id is ", order_id)
cancel, err = tda.cancel_order(account_id=os.environ["tda_order_account"], order_id=order_id, jsonify=False)
print("the order has been cancelled")
print(cancel.headers)
