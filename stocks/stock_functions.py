import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

# dict to store parabola's equations
equations_min = {"a": [], "b": [], "c": []}
equations_max = {"a": [], "b": [], "c": []}


# FUNCTIONS
def relative_min(z, first, min_values, max_values):
    try:
        if first == "MIN":
            variation = min_values["Second"][z] - max_values["Second"][z-1]
        else:
            variation = min_values["Second"][z] - max_values["Second"][z]

    # This error will appear when one minimum is missed, thus imperceptible
    # so this min is more or less equal to the halfway point between one min and the last one
    except IndexError:
        variation = (min_values["Second"][z] + min_values["Second"][z - 1])/2

    # MINIMUM VALUES
    # minimum point of the parabola
    i, j = min_values['Second'][z], min_values["Price"][z]

    # find a,b,c from ax^2+bx+c
    a = pow(math.e, 1 / variation)
    b, c = -2 * a * i, j + a * pow(i, 2)

    # append a, b, c from ax^2 + bx + c to an array
    equations_min["a"].append(a)
    equations_min["b"].append(b)
    equations_min["c"].append(c)

    # plot parabola
    points = np.linspace(min_values["Second"][z] - 10, min_values["Second"][z] + 10, 1000)
    plt.plot(points, a * points**2 + b * points + c, label='function')


def relative_max(z, first, min_values, max_values):
    try:
        if first == "MAX":
            variation = max_values["Second"][z] - min_values["Second"][z-1]
        else:
            variation = max_values["Second"][z] - min_values["Second"][z]

    # This error will appear when one minimum is missed, thus imperceptible
    # so this min is more or less equal to the halfway point between one max and the last one
    except IndexError:
        variation = (max_values["Second"][z] + max_values["Second"][z-1])/2

    # MAXIMUM VALUES
    # max point of the parabola
    i, j = max_values['Second'][z], max_values['Price'][z]

    # find a,b,c from ax^2 + bx + c (system of equations)
    a = - pow(math.e, 1 / variation)
    b, c = -2 * a * i, j + a * pow(i, 2)

    # append a, b, c from ax^2 + bx+ c to an array
    equations_max["a"].append(a)
    equations_max["b"].append(b)
    equations_max["c"].append(c)

    # plot parabola
    points = np.linspace(max_values['Second'][z] - 10, max_values['Second'][z] + 10, 1000)
    plt.plot(points, a * points**2 + b * points + c, label='function2')


def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx - 1]) < math.fabs(value - array[idx])):
        return array[idx - 1]
    else:
        return array[idx]

