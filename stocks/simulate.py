import requests
from data_simulation import *
from time import sleep
from scan_simulation import *

dicta = {"Second": [],
         "Price": []}

max = int(input("\nSeconds to record the fluctuation: "))
i = 0
# request the price
while i < max:
    print(i, end=", ")
    url = requests.get(f'https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT')
    data_btc = url.json()
    actual_price = float(data_btc['price'])
    dicta["Price"].append(actual_price)
    dicta["Second"].append(i)

    sleep(1)
    # find next value in order to determine if the last is a max or min
    url = requests.get(f'https://api.binanc5e.com/api/v1/ticker/price?symbol=BTCUSDT')
    data_btc = url.json()
    next_value = float(data_btc['price'])

    data(dicta, i, next_value)

    try:
        scan_point(i, actual_price)
    except IndexError:
        pass
    i += 1

print()
print(dicta)
print(max_values)
print(min_values)

plot_stock_graph(dicta, max_values, min_values)
