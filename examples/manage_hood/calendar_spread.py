
class CalendarSpread:
    def __init__(self, front_leg_option, back_leg_option):
        self.front_leg_option = front_leg_option
        self.back_leg_option = back_leg_option

    def get_front_leg_option(self):
        return self.front_leg_option

    def get_back_leg_option(self):
        return self.back_leg_option

    def get_leg_spread(self):
        bid_price = self.front_leg_option.get("bid_price")
        ask_price = self.back_leg_option.get("ask_price")

        if (ask_price and bid_price):
            return float(ask_price) - float(bid_price)

        return None

    def is_placeable(self):
        bid_price = self.front_leg_option.get("bid_price")
        ask_price = self.back_leg_option.get("ask_price")

        if (ask_price and bid_price):
            return True

        return False

    def print(self):
        print(self.front_leg_option.get("type"),
            self.front_leg_option.get("strike_price"),
            self.front_leg_option.get("expiration_date"),
            self.back_leg_option.get("expiration_date"),
            self.get_leg_spread())
