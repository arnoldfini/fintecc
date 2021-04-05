from data_simulation import *
from time import sleep
from scan_simulation import *
import os
import requests
from binance.client import Client

# init
#api_key = os.environ.get('binance_api')
#api_secret = os.environ.get('binance_secret')
#client = Client(api_key, api_secret)
demo_api_key = "O8n9KgnF6WCzFEQE2tcbGPPXEoMHuJYWkF01jzl3D8nB5csTHUHzE7eh7oBzLGli"
demo_api_secret = "HNd8AuYeLikCBsGHsaZ4iOVKjCG5MpnmanKGkceVdv5NGv16M8Ua46D1vk6aH6E6"
client = Client(demo_api_key, demo_api_secret)
client.API_URL = 'https://testnet.binance.vision/api'

# You ask for the balance
balance = client.get_asset_balance(asset='USDT')
usdt = balance['free']
print(round(float(client.get_asset_balance(asset='USDT')['free'])/float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT").json()["price"]), 6))
client.order_market_sell(symbol='ETHUSDT', quantity=100)

print(client.get_asset_balance(asset="ETH")['free'], client.get_asset_balance(asset="USDT")['free'])
exit()
# TODO Create balance in order to see the gains and losses of the algorithm in real time
crypto_info = {"Second": [],
               "Price": []}

crypto = input("Symbol: ")
symbol = crypto.upper() + "USDT"
print(symbol)
max = int(input("Seconds to record the fluctuation: "))
init = client.get_asset_balance(asset='USDT')['free']
init1 = client.get_asset_balance(asset=crypto)['free']
print(init, init1)

# If I have no usdt in my account sell other crypto
if float(usdt) == 0.:
    client.create_test_order(
        symbol=symbol,
        side='SELL',
        type='LIMIT',
        timeInForce='GTC',
        quantity=round(client.get_asset_balance(asset=crypto)['free'],6),
        price=float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}").json()["price"]))

print(client.get_asset_balance(asset='USDT')['free'])

i = 0
# request the price
while i < max:

    actual_price = float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}").json()["price"])
    print(actual_price)
    crypto_info["Price"].append(actual_price)
    crypto_info["Second"].append(i)

    sleep(1)
    # find next value in order to determine if the last is a max or min
    next_value = float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}").json()["price"])

    data(crypto_info, i, next_value)

    try:
        order = scan_point(crypto_info, i, actual_price)
        if order == 0:
            if usdt != 0:
                client.create_test_order(
                    symbol=symbol,
                    side='BUY',
                    type='LIMIT',
                    timeInForce='GTC',
                    quantity=round(float(client.get_asset_balance(asset='USDT')['free'])/actual_price, 6),
                    price=actual_price)
            else:
                pass
        elif order == 1:
            client.create_test_order(
                symbol=symbol,
                side='SELL',
                type='LIMIT',
                timeInForce='GTC',
                quantity=round(float(client.get_asset_balance(asset='USDT')['free'])/actual_price,6),
                price=actual_price)

    except IndexError:
        pass
    i += 1


benefit = float(client.get_asset_balance(asset='USDT')['free']) - float(init)
print(f"Benefit: {benefit}")
print(f"Money: {client.get_asset_balance(asset='USDT')['free']}")

print()
print(crypto_info)
print(max_values)
print(min_values)

plot_stock_graph(crypto_info, max_values, min_values)
