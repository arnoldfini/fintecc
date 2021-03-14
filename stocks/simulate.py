from data_simulation import *
from time import sleep
from scan_simulation import *
import os
from binance.client import Client

# init
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client = Client(api_key, api_secret)

# TODO Create balance in order to see the gains and losses of the algorithm in real time
crypto = {"Second": [],
          "Price": []}

max = int(input("Seconds to record the fluctuation: "))
i = 0
# request the price
while i < max:
    actual_price = float(client.get_symbol_ticker(symbol="BTCUSDT")["price"])
    crypto["Price"].append(actual_price)
    crypto["Second"].append(i)

    sleep(1)
    # find next value in order to determine if the last is a max or min
    next_value = float(client.get_symbol_ticker(symbol="BTCUSDT")["price"])

    data(crypto, i, next_value)

    try:
        scan_point(crypto, i, actual_price)
    except IndexError:
        pass
    i += 1

print()
print(crypto)
print(max_values)
print(min_values)

plot_stock_graph(crypto, max_values, min_values)
