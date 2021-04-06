import requests
import math

'''
File to store functions that fire orders (buy, sell, limit...)
'''


class Crypto:
    def __init__(self, crypto):
        self.crypto = str(crypto).upper().strip()
        self.balance = 1000  # quantity of this crypto is 1000 USDT
        self.balance_copy = self.balance
        # buy price of a given crypto
        self.buy_price = 0
        # before selling, something must have been bought in the first place hence we have to check
        self.bought = False
        self.quantity_bought = 1
        self.benefit = 0

    def price(self):
        try:
            # getting the request from url
            info = requests.get(f"https://data.messari.io/api/v1/assets/{self.crypto}/metrics")
            return float(info.json()["data"]["market_data"]["price_usd"])
        except:
            info = requests.get(f"https://api.binance.com/api/v1/ticker/price?symbol={self.crypto}USDT")
            return float(info.json()["price"])

    def buy(self, derivative):
        # TODO if there are a lot of buys at the same time compound them

        # if it has bought before return
        if self.bought:
            return

        # the quantity bought is the ratio of this function that it slowly tends to 1 in the limit
        # hence as bigger derivative, bigger ratio, bigger quantity bought
        self.quantity_bought = derivative / (derivative + 8)

        actual_price = self.price()
        self.buy_price = actual_price
        self.bought = True

    def sell(self):
        if not self.bought:
            return

        actual_price = self.price()
        profit = actual_price / self.buy_price

        # Calculate the profit only with the spent part
        not_spent = self.balance - self.quantity_bought * self.balance
        print(f"Balance before: {self.balance}, Bought: {self.quantity_bought * self.balance}, Profit: {profit}, "
              f"Not_spent: {not_spent}", end=", ")
        self.balance = (self.quantity_bought * self.balance) * profit + not_spent
        print(f"Balance after: {self.balance}")

        self.benefit += self.balance - 1000

        self.bought = False

