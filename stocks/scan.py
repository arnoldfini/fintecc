import numpy as np
import pandas
import math
from stock_functions import *
from data import *

data = data()


def scan_point(x, y):
    # for a point x,y find its correspondent parabola

    # this point is in the middle of one max and one min
    # so finding one max and one min and look what point is nearer
    closest_max_min = [find_nearest(max_values["Second"], x),
                       find_nearest(min_values["Second"], x)]

    # stationary point of the parabola
    parabola_stationary = min(closest_max_min)

    # point i,j of the stationary point
    try:
        i, j = parabola_stationary, min_values["Price"][min_values["Second"].index(parabola_stationary)]
    except ValueError:
        i, j = parabola_stationary, max_values["Price"][max_values["Second"].index(parabola_stationary)]

    # equation of the type ax^2 + bx + c = 0
    for z in range(len(equations["max"]["a"])):
        a = equations["max"]["a"][z]
        b, c = -2 * a * i, j + a * i**2

        if equations["max"]["b"][z] == b and equations["max"]["c"][z] == c:
            break

        a = equations["min"]["a"][z]
        b, c = -2 * a * i, j + a * i ** 2

        if equations["min"]["b"][z] == b and equations["min"]["c"][z] == c:
            break

    # point y that maps to the parabola: f(x)
    y_parabola = a * (x ** 2) + b * x + c

    # try to find a solution, if not the parabola is not following the tendency so it's time to sell/buy
    try:
        # check if discriminant equals 0 -> y is the tangent line of the parabola
        # thus it must be a max or min
        if round(b ** 2 - 4 * a * (c - y)) == 0:
            if a > 0:
                x_parabola = int(x)
                print(f"Buy: ({x}, {y})")
                return
            elif a < 0:
                x_parabola = int(x)
                print(f"Sell: ({x}, {y})")
                return
        else:
            # point x that maps to the parabola: ax^2 + bx + c = y -> ax^2 + bx + (c-y) = 0
            x_parabola = [(-b + math.sqrt(b ** 2 - 4 * a * (c - y))) / 2 * a,
                          (-b - math.sqrt(b ** 2 - 4 * a * (c - y))) / 2 * a]

    except ValueError:
        # for a point
        # if completely breaks parabola's path (there's no solution for y in that point), buy or sell depending on "a"
        if a > 0:
            print(f"Sell: ({x}, {y})")
            return
        elif a < 0:
            print(f"Buy: ({x}, {y})")
            return

    # ratio of point to the parabola which indicates the slope
    try:
        dx = x - max(x_parabola)
        dy = y - y_parabola
        ratio = dy / dx
    except TypeError:
        # if it's tangent the ratio is 0 because it's in the parabola
        ratio = 0

    # if the ratio <= 5 means that the point is very near to the parabola, so the derivative is more or less equal
    if int(ratio) <= 3:
        derivative = 2 * x * a + b

        # if in the same parabola the derivative is either very negative or positive, buy or sell
        if derivative > 8:
            print(f"Buy: ({x}, {y}) by derivative {derivative}")
            return
        elif derivative < -8:
            print(f"Sell: ({x}, {y}) by derivative {derivative}")
            return

        else:
            # when the graph doesn't really follow the parabola tendency, create a slope with the last value
            # if slope is really big, buy. otherwise sell
            dy, dx = y - df["Price"][x-1], x - df["Second"][x-1]
            try:
                # By weird mathematics this is the approximation of the slope (in mafs.png)
                slope = math.tan(np.arcsin(math.sqrt(int(3 * (dy**2) - dx**2)) / 2 * dx))

            except ValueError:
                # This happens when last value is slightly bigger but not a maximum or minimum
                # As it's *slightly* bigger just don't do nothing, it's fine because it's flat
                return

            if slope > 8:
                print(f"Buy: ({x}, {y}) by derivative {derivative}")
                return
            elif slope < -8:
                print(f"Sell: ({x}, {y}) by derivative {derivative}")
                return
            else:
                # Don't do nothing
                return

    return

for i in range(1, len(df),10):
    scan_point(df["Second"][i], df["Price"][i])

plot_stock_graph(data[0], data[1])