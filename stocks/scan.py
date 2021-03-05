import numpy as np
import pandas

def scan_point(x, y):
    # for a point x,y find its correspondent parabola
    # this point is in the middle of one max and one min
    # so finding one max and one min and look what point is nearer
    # TODO Comment
    tmp = []
    tmp.append(max_values["Second"][(np.abs(max_values["Second"] - x)).argmin()])
    tmp.append(min_values["Second"][(np.abs(min_values["Second"] - x)).argmin()])

    # stationary point of the parabola
    parabola_stationary = min(tmp)

    # TODO Comment
    try:
        i, j = parabola_stationary, min_values["Second"][min_values["Second"].index(parabola_stationary)]
    except ValueError:
        i, j = parabola_stationary, max_values["Second"][max_values["Second"].index(parabola_stationary)]

    for i in range(len(equations_max["a"])):
        a = equations_max["a"][i]
        a, b, c = equations_max["a"][i], -2 * a * i, j + a * pow(i, 2)
        if equations_max["b"][i] == -2*a*i and equations_max["c"][i] == j + a * pow(i, 2):
            print(a, b, c)
            break

    # equation of the type ax^2 + bx + c = 0
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
            # sell()
            pass
        elif a < 0:
            print(f"Buy: ({x}, {y})")
            # buy()
            pass
        return

    # ratio of point to the parabola which indicates the slope
    dy = y - y_parabola
    dx = x - max(x_parabola)
    ratio = dy / dx

    # if the ratio <= 5 means that the point is very near to the parabola, so the derivative is more or less equal
    if int(ratio) <= 5:
        derivative = 2 * x * a + b

        # if in the same parabola the derivative is either very negative or positive, buy or sell
        if derivative > 10:
            print(f"Buy: ({x}, {y})")
            # buy()
            pass
        elif derivative < -10:
            print(f"Sell: ({x}, {y})")
            # sell()
            pass

    else:
        # TODO: what happens when the graph doesn't really follow the parabola tendency
        pass

    return