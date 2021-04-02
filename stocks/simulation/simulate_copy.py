from data_simulation import *
from time import sleep
from scan_simulation import *
import os
from orders import *

# Dict of prices & seconds
info = {"Second": [],
        "Price": []}

# Info of the crypto and a class assigned in order to buy/sell
crypto_id = input("Crypto: ")
symbol = crypto_id + "USDT"
# create crypto object
crypto = Crypto(crypto_id)

seconds = int(input("Seconds to record the fluctuation: "))
i = 0
# request the price
while i < seconds:
    actual_price = crypto.price()
    info["Price"].append(actual_price)
    info["Second"].append(i)

    sleep(1)
    # find next value in order to determine if the last is a max or min
    next_value = crypto.price()

    data(info, i, next_value)
    try:
        order = scan_point(info, i, actual_price)

        if order == 0:
            crypto.buy()

        elif order == 1:
            crypto.sell()

    except IndexError:
        pass

    i += 1

# TODO
benefit = crypto.balance - 1000
print(f"Benefit: {benefit}")
print(f"Money: {crypto.balance}")

print()
print(info)
print(max_values)
print(min_values)

plot_stock_graph(info, max_values, min_values)