import pandas as pd
from matplotlib import pyplot as plt
import math
import numpy as np

df = pd.read_csv("bitcoin_price.csv")
price = df['Price']
x = [i for i in range(len(df))]

# dict of relative max values and min values
max_values = {"Second": [], "Price": []}
min_values = {"Second": [], "Price": []}

for i in range(len(price)-1):
    # Locate first max or min
    if i == 0:
        if price[i] > price[i+1]:
            max_values["Second"].append(df['Second'][i])
            max_values["Price"].append(price[i])
        elif price[i] < price[i+1]:
            min_values["Second"].append(df["Second"][i])
            min_values["Price"].append(price[i])
    # See if its a relative max
    elif price[i] > price[i-1] and price[i] > price[i+1]:
        max_values["Second"].append(df['Second'][i])
        max_values["Price"].append(price[i])
    # See if its a relative min
    elif price[i] < price[i-1] and price[i] < price[i+1]:
        min_values["Second"].append(df["Second"][i])
        min_values["Price"].append(price[i])

# Create df from max_values
df_max = pd.DataFrame(max_values)
df_min = pd.DataFrame(min_values)

# from parabola equation (ax^2+bx+c)
variation = min_values["Second"][0] - df_max["Second"][0]
a = pow(math.e, variation)

# minimum point of the parabola
i, j = min_values['Second'][0], df_min["Price"][0]

# find b,c from ax^2+bx+c
matrix = np.array([[i, 1], [1, 0]])
values = np.array([[j - (a * pow(i, 2))], [-2 * a * i]])
b, c = np.linalg.inv(matrix) @ values

# plot parabola
p = np.linspace(df_max["Second"][0], df_max["Second"][1], 1000)
plt.plot(p, a*pow(p, 2) + b*p + c, label='function')

# plot stock graph
plt.plot(x, price, label='stock')
plt.scatter(df_max["Second"], df_max["Price"], color='r')
plt.scatter(df_min["Second"], df_min["Price"], color='b')
plt.plot(x, price)
plt.xlabel('Time')
plt.ylabel('Price')
plt.show()
