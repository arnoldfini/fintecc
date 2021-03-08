import pandas as pd
import matplotlib.pyplot as plt
from stock_functions import *

df = pd.read_csv("bitcoin_price.csv", header=0)
price = df['Price']
x = [i for i in range(len(df))]

# dict of relative max values and min values
max_values = {"Second": [], "Price": []}
min_values = {"Second": [], "Price": []}

for i in range(len(price)-1):
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

#for i in range(1, len(df)):
#    scan_point(df["Second"][i], df["Price"][i])

# plot stock graph
plt.plot(x, price, label='stock')
plt.scatter(max_values["Second"], max_values["Price"], color='r')
plt.scatter(min_values["Second"], min_values["Price"], color='b')
plt.plot(x, price)
plt.xlabel('Time')
plt.ylabel('Price')
plt.show()