import pandas as pd
from matplotlib import pyplot as plt
import math
import numpy as np

# Function that for one point on the stock graph, returns the ratio of tangency to the parabola
# time and price correspond to x,y in stock graph.
# values are the parabola points
#def tangency(time , price, values):

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
for z in range(2):
    # Arrays to store parabola's equations
    equations_min = {"a": [], "b": [], "c": []}
    equations_max = {"a": [], "b": [], "c": []}

    # from parabola equation (ax^2+bx+c)
    variation = min_values["Second"][z] - df_max["Second"][z]

    # MINIMUM VALUES
    # minimum point of the parabola
    i, j = min_values['Second'][z], df_min["Price"][z]

    # find a,b,c from ax^2+bx+c
    a = pow(math.e, 1/variation)
    b, c = -2 * a * i, j + a * pow(i, 2)

    # append a, b, c from ax^2 + bx + c to an array
    equations_min["a"].append(a)
    equations_min["b"].append(b)
    equations_min["c"].append(c)

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
    equations_max["a"].extend(a)
    equations_max["b"].extend(b)
    equations_max["c"].extend(c)

    print(equations_max)

    # plot parabola
    points = np.linspace(df_max['Second'][z]-10, df_max['Second'][z+1]+10, 1000)
    plt.plot(points, a * pow(points, 2) + b*points + c, label='function2')

print(equations_max)

# plot stock graph
plt.plot(x, price, label='stock')
plt.scatter(df_max["Second"], df_max["Price"], color='r')
plt.scatter(df_min["Second"], df_min["Price"], color='b')
plt.plot(x, price)
plt.xlabel('Time')
plt.ylabel('Price')
plt.show()

###

# point
x, y = df["Second"][2], df["Price"][2]

# equation of the type ax^2 + bx + c = 0
a, b, c = equations_max["a"][0], equations_max["b"][0], equations_max["c"][0]

# point y that maps to the parabola: f(x)
y_parabola = a*(x**2) + b*x + c

# point x that maps to the parabola: ax^2 + bx + c = y -> ax^2 + bx + (c-y) = 0
x_parabola_1 = (-b + math.sqrt(b**2 - 4 * a * (c-y)))/2 * a
x_parabola_2 = (-b - math.sqrt(b**2 - 4 * a * (c-y)))/2 * a

# ratio of point to the parabola which indicates the slope
dy = y - y_parabola
dx = x - x_parabola_2
ratio = dy/dx

# if the ratio <= 5 means that the point is very near to the parabola, so the derivative is more or less equal
if int(ratio) <= 5:
    derivative = 2*x*a + b

# if in the same parabola the derivative is either very negative or positive, buy or sell
if derivative > 10:
    # buy()
    pass
elif derivative < -10:
    # sell()
    pass
