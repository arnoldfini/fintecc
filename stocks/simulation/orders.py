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
        self.buy_iterations = 1
        self.quantity_bought = 1
        self.compound = []
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
        # if it has bought before return
        if self.bought:
            return

        # buy compounding quantities each time (compounding interest divided by e, meaning in the limit
        # the function tends to 1 which is exactly the whole quantity of self.balance that is being used
        # then multiply by the derivative so bigger dips can be obtained
        self.quantity_bought = (((1 + 1/self.buy_iterations) ** self.buy_iterations)/math.e) * derivative
        self.compound.append(self.quantity_bought)
        self.buy_iterations += 1

        actual_price = self.price()
        self.buy_price = actual_price
        self.bought = True

    def sell(self):
        if not self.bought:
            return

        actual_price = self.price()
        profit = actual_price / self.buy_price

        # Calculate the profit only with the spent part
        # the sum of all compounds sum(hi-hi-1) = hn -> last element of the array
        sum = self.compound[len(self.compound)-1]

        not_spent = self.balance - sum * self.balance
        print(f"Balance before: {self.balance}, Sum: {sum * self.balance}, Profit: {profit}, Not_spent: {not_spent}", end=", ")
        self.balance = (sum * self.balance) * profit + not_spent
        print(f"Balance after: {self.balance}")

        self.benefit += self.balance - 1000

        self.bought = False

