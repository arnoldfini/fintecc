from data_simulation import *
from time import sleep
from scan_simulation import *
import os
from binance.client import Client
from orders import *


# init
#api_key = os.environ.get('binance_api')
#api_secret = os.environ.get('binance_secret')
#client = Client(api_key, api_secret)
demo_api_key = "zPXQy2mWVBBFcKAsbibqLKhGNR6adL41AeQDLf6Fzf9kyNIqbEPjhCNLhbKxw0Rz"
demo_api_secret = "H5SFI4ZQoQfPCsHaZIMSkdDL8KPnQFq3w072Fyx6Bc9L2XZFxakdSb6gXcI4DjpN"
client = Client(demo_api_key, demo_api_secret)
client.API_URL = 'https://testnet.binance.vision/api'


# TODO Create balance in order to see the gains and losses of the algorithm in real time
crypto = {"Second": [],
          "Price": []}
symbol = input("Symbol: ").upper() + "USDT"

max = int(input("Seconds to record the fluctuation: "))



# If I have no usdt in my account sell other crypto
if float(usdt) == 0.:
    client.create_test_order(
        symbol=symbol,
        side='SELL',
        type='LIMIT',
        timeInForce='GTC',
        quantity=float(client.get_symbol_ticker(symbol=symbol)["price"]),
        price=float(client.get_symbol_ticker(symbol=symbol)["price"]))

print(client.get_asset_balance(asset='USDT')['free'])
i = 0
# request the price
while i < max:
    actual_price = float(client.get_symbol_ticker(symbol=symbol)["price"])
    crypto["Price"].append(actual_price)
    crypto["Second"].append(i)

    sleep(1)
    # find next value in order to determine if the last is a max or min
    next_value = float(client.get_symbol_ticker(symbol=symbol)["price"])

    data(crypto, i, next_value)
    try:
        order = scan_point(crypto, i, actual_price)

    except IndexError:
        pass

    '''try:
        if order == 0:
            if usdt != 0:
                client.create_test_order(
                    symbol=symbol,
                    side='BUY',
                    type='LIMIT',
                    timeInForce='GTC',
                    quantity=float(client.get_asset_balance(asset='USDT')['free'])/actual_price,
                    price=actual_price)
            else:
                pass
        elif order == 1:
            client.create_test_order(
                symbol=symbol,
                side='SELL',
                type='LIMIT',
                timeInForce='GTC',
                quantity=float(client.get_asset_balance(asset='USDT')['free'])/actual_price,
                price=actual_price)

    except IndexError:
        pass'''
    i += 1


benefit = float(client.get_asset_balance(asset='USDT')['free']) - float(init)
print(f"Benefit: {benefit}")
print(f"Money: {client.get_asset_balance(asset='USDT')['free']}")

print()
print(crypto)
print(max_values)
print(min_values)

plot_stock_graph(crypto, max_values, min_values)