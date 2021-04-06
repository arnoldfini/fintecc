from orders import *
from scan import *
import pandas as pd
from stock_functions import *
from scan import *

# TODO If there are two equal consecutive values what to do (Ex: bitcoin_price1.csv, Second = 82)

df = pd.read_csv("bitcoin_price1.csv", header=0)
price = df['Price']

# dict of relative max values and min values
max_values = {"Second": [], "Price": []}
min_values = {"Second": [], "Price": []}


def data():
    for i in range(len(price) - 1):
        # Locate first max or min, also don't count noise maximums or minimums
        if i == 0:
            if price[i] > price[i + 1] and int(price[i] - price[i + 1]) != 0:
                max_values["Second"].append(df['Second'][i])
                max_values["Price"].append(price[i])
                # Track if first element is max
                first = "MAX"
            else:
                min_values["Second"].append(df["Second"][i])
                min_values["Price"].append(price[i])
                # Track if first element is min
                first = "MIN"

        # See if its a relative max
        elif price[i] > price[i - 1] and price[i] > price[i + 1]:
            max_values["Second"].append(df['Second'][i])
            max_values["Price"].append(price[i])
            relative_max(max_values["Second"].index(i), first, min_values, max_values)

        # See if its a relative min
        elif price[i] < price[i - 1] and price[i] < price[i + 1]:
            min_values["Second"].append(df["Second"][i])
            min_values["Price"].append(price[i])
            relative_min(min_values["Second"].index(i), first, min_values, max_values)

    return max_values, min_values


def plot_stock_graph(max_values, min_values):
    x = [i for i in range(len(df))]

    # plot stock graph
    plt.plot(x, price, label='stock')
    plt.scatter(max_values["Second"], max_values["Price"], color='r')
    plt.scatter(min_values["Second"], min_values["Price"], color='b')
    plt.plot(x, price)
    plt.xlabel('Time')
    plt.ylabel('Price')
    return plt.show()


maxim, minim = data()

crypto = Crypto("BTC")
for i in range(len(df)):
    order = scan_point(df, df["Second"][i], df["Price"][i])
    # TODO buy/sell depending on DERIVATIVE
    if order[0] == 0:
        if len(order) == 2:
            crypto.buy(order[1])
        else:
            crypto.buy(1)
    elif order[0] == 1:
        crypto.sell()



print(f"Benefit in BTC: {crypto.benefit / crypto.price()}, Benefit in USDT: {crypto.benefit}")
print(f"Money: {crypto.balance / crypto.price()} BTC, {crypto.balance} USDT")

print()
print(df)
print(max_values)
print(min_values)

plot_stock_graph(data[0], data[1])
