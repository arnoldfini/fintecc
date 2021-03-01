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
    # Locate first max or min, also don't count noise maximums or minimums
    if i == 0:
        if price[i] > price[i+1] and int(price[i] - price[i+1]) != 0:
            max_values["Second"].append(df['Second'][i])
            max_values["Price"].append(price[i])
        else:
            min_values["Second"].append(df["Second"][i])
            min_values["Price"].append(price[i])
    # See if its a relative max
    elif price[i] > price[i-1] and price[i] > price[i+1] and int(price[i] - price[i+1]) != 0 and int(price[i] - price[i-1]) != 0:
        max_values["Second"].append(df['Second'][i])
        max_values["Price"].append(price[i])
    # See if its a relative min
    elif price[i] < price[i-1] and price[i] < price[i+1] and int(price[i+1] - price[i]) != 0 and int(price[i-1] - price[i]) != 0:
        min_values["Second"].append(df["Second"][i])
        min_values["Price"].append(price[i])

# Create df from max_values
df_max = pd.DataFrame(max_values)
df_min = pd.DataFrame(min_values)

# plot parabola for max and min values
for z in range(3):
    # Arrays to store parabola's equations
    equations_min = [[], [], []]
    equations_max = [[], [], []]

    # from parabola equation (ax^2+bx+c)
    variation = min_values["Second"][z] - df_max["Second"][z]

    # MINIMUM VALUES
    # minimum point of the parabola
    i, j = min_values['Second'][z], df_min["Price"][z]

    # find a,b,c from ax^2+bx+c
    a = pow(math.e, 1/variation)
    b, c = -2 * a * i, j + a * pow(i, 2)

    # append a, b, c from ax^2 + bx + c to an array
    equations_min[0].append(a)
    equations_min[1].append(b)
    equations_min[2].append(c)

    # plot parabola
    points = np.linspace(df_min["Second"][z]-10, df_min["Second"][z+1]+10, 1000)
    plt.plot(points, a*pow(points, 2) + b*points + c, label='function')

    # MAXIMUM VALUES
    # max point of the parabola
    i, j = max_values['Second'][z], df_max['Price'][z]

    # find a,b,c from ax^2 + bx + c (system of equations)
    a = - pow(math.e, 1 / variation)
    b, c = -2 * a * i, j + a * pow(i, 2)

    # append a, b, c from ax^2 + bx+ c to an array
    equations_max[0].append(a)
    equations_max[1].append(b)
    equations_max[2].append(c)

    print(a, b, c)

    # plot parabola
    points = np.linspace(df_max['Second'][z]-10, df_max['Second'][z+1]+10, 1000)
    plt.plot(points, a * pow(points, 2) + b*points + c, label='function2')

# plot stock graph
plt.plot(x, price, label='stock')
plt.scatter(df_max["Second"], df_max["Price"], color='r')
plt.scatter(df_min["Second"], df_min["Price"], color='b')
plt.plot(x, price)
plt.xlabel('Time')
plt.ylabel('Price')
plt.show()
