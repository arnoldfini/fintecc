import requests
from bs4 import BeautifulSoup as BS

'''
File to store functions that fire orders (buy, sell, limit...)
'''


class Crypto:
    def __init__(self, crypto):
        self.crypto = str(crypto).upper().strip()
        self.quantity = 1000/self.price()  # quantity of this crypto is 1000 USDT, which is 1000/price of any crypto
        self.balance = self.quantity * self.price()  # balance of this crypto
        # buy price of a given crypto
        self.buy_price = 0
        # before selling, something must have been bought in the first place hence we have to check
        self.bought = False

    def price(self):
        # getting the request from url
        info = requests.get(f"https://data.messari.io/api/v1/assets/{self.crypto}/metrics")
        print(info.json())
        return float(info.json()["data"]["market_data"]["price_usd"])

    def buy(self):
        # if it has bought before return
        if self.bought:
            return

        actual_price = self.price()
        self.buy_price = actual_price
        self.bought = True

    def sell(self):
        if not self.bought:
            return

        actual_price = self.price()
        profit = actual_price / self.buy_price
        self.balance = self.balance * profit
        self.bought = False
