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

for i in range(len(price) - 1):
    # Locate first max or min, also don't count noise maximums or minimums
    if i == 0:
        if price[i] > price[i + 1] and int(price[i] - price[i + 1]) != 0:
            max_values["Second"].append(df['Second'][i])
            max_values["Price"].append(price[i])
        else:
            min_values["Second"].append(df["Second"][i])
            min_values["Price"].append(price[i])
    # See if its a relative max
    elif price[i] > price[i - 1] and price[i] > price[i + 1] and int(price[i] - price[i + 1]) != 0 and int(
            price[i] - price[i - 1]) != 0:
        max_values["Second"].append(df['Second'][i])
        max_values["Price"].append(price[i])
    # See if its a relative min
    elif price[i] < price[i - 1] and price[i] < price[i + 1] and int(price[i + 1] - price[i]) != 0 and int(
            price[i - 1] - price[i]) != 0:
        min_values["Second"].append(df["Second"][i])
        min_values["Price"].append(price[i])

# Create df from max_values
df_max = pd.DataFrame(max_values)
df_min = pd.DataFrame(min_values)

# 2*n parabolas
n = 1

# plot parabola for max and min values
for z in range(n):
    # Arrays to store parabola's equations
    equations_min = {"a": [], "b": [], "c": []}
    equations_max = {"a": [], "b": [], "c": []}

    # from parabola equation (ax^2+bx+c)
    variation = max_values["Second"][z] - min_values["Second"][z]

    # MINIMUM VALUES
    # minimum point of the parabola
    i, j = min_values['Second'][z], df_min["Price"][z]

    # find a,b,c from ax^2+bx+c
    a = pow(math.e, 1 / variation)
    b, c = -2 * a * i, j + a * pow(i, 2)

    # append a, b, c from ax^2 + bx + c to an array
    equations_min["a"].append(a)
    equations_min["b"].append(b)
    equations_min["c"].append(c)

    # plot parabola
    points = np.linspace(df_min["Second"][z] - 10, df_min["Second"][z + 1] + 10, 1000)
    plt.plot(points, a * pow(points, 2) + b * points + c, label='function')

for i in range(n):
    # MAXIMUM VALUES
    # max point of the parabola
    i, j = max_values['Second'][z], df_max['Price'][z]

    # from parabola equation (ax^2+bx+c)
    variation = min_values["Second"][z] - max_values["Second"][z]

    # find a,b,c from ax^2 + bx + c (system of equations)
    a = - pow(math.e, 1 / variation)
    b, c = -2 * a * i, j + a * pow(i, 2)

    # append a, b, c from ax^2 + bx+ c to an array
    equations_max["a"].append(a)
    equations_max["b"].append(b)
    equations_max["c"].append(c)

    # plot parabola
    points = np.linspace(df_max['Second'][z] - 10, df_max['Second'][z + 1] + 10, 1000)
    plt.plot(points, a * pow(points, 2) + b * points + c, label='function2')

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


def scan_point(x, y):
    # for a point x,y find its correspondent parabola
    # this point is in the middle of one max and one min
    # so finding one max and one min and look what point is nearer
    tmp = []
    for maximum in max_values["Second"]:
        if int(maximum - x) == 0:
            tmp.append(maximum-x)
    for minimum in min_values["Second"]:
        if int(minimum - x) == 0:
            tmp.append(minimum-x)

    # stationary point of the parabola
    parabola_stationary = min(tmp)
    
    i, j = parabola_stationary, min_values["Second"][min_values["Price"].index(parabola_stationary)]
    b, c = -2 * a * i, j + a * pow(i, 2)
    for i in range(len(equations_max["a"])):
        a_tmp = equations_max["a"][i]
        if equations_max["b"][i] == b/a_tmp and equations_max["c"][i] == c - a_tmp:
            a = equations_max["a"][i]

    # equation of the type ax^2 + bx + c = 0
    global derivative
    a, b, c = equations_max["a"][0], equations_max["b"][0], equations_max["c"][0]

    # point y that maps to the parabola: f(x)
    y_parabola = a * (x ** 2) + b * x + c

    # try to find a solution, if not the parabola is not following the tendency so it's time to sell/buy
    try:
        # point x that maps to the parabola: ax^2 + bx + c = y -> ax^2 + bx + (c-y) = 0
        x_parabola = [(-b + math.sqrt(b ** 2 - 4 * a * (c - y))) / 2 * a,
                      (-b - math.sqrt(b ** 2 - 4 * a * (c - y))) / 2 * a]
    except ValueError:
        # for a point
        # if completely breaks parabola's path (there's no solution for y in that point), buy or sell depending on "a"
        if a > 0:
            print(f"Sell: ({x}, {y})")
            pass
        elif a < 0:
            print(f"Buy: ({x}, {y})")
            pass
        return

    # ratio of point to the parabola which indicates the slope
    dy = y - y_parabola
    dx = x - max(x_parabola)
    ratio = dy / dx

    # if the ratio <= 5 means that the point is very near to the parabola, so the derivative is more or less equal
    if int(ratio) <= 5:
        derivative = 2 * x * a + b
    else:
        # TODO: what happens when the graph doesn't really follow the parabola tendency
        pass
    if derivative > 10:
        print(f"Buy: ({x},{y})")
        pass
    elif derivative < -10:
        print(f"Sell: ({x},{y})")
        pass

    # if in the same parabola the derivative is either very negative or positive, buy or sell

    return

scan_point(x, y)