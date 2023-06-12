import robin_stocks.robinhood as rh
import variables
import pyotp

login = rh.login(variables.RH_Login, variables.RH_Pass, store_session=True)
totp = pyotp.TOTP("My2FApp").now()
print("Current OTP:", totp)

data = rh.load_phoenix_account()
print(data)

