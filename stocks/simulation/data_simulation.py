from stocks.stock_functions import *

# TODO If there are two equal consecutive values what to do (Ex: bitcoin_price1.csv, Second = 82)

# dict of relative max values and min values
max_values = {"Second": [], "Price": []}
min_values = {"Second": [], "Price": []}


def data(df, i, next_value):
    global first
    # Locate first max or min, also don't count noise maximums or minimums
    if i == 0:
        if df["Price"][i] > next_value and int(df["Price"][i] - next_value) != 0:
            max_values["Second"].append(df['Second'][i])
            max_values["Price"].append(df["Price"][i])
            # Track if first element is max
            first = "MAX"
        else:
            min_values["Second"].append(df["Second"][i])
            min_values["Price"].append(df["Price"][i])
            # Track if first element is min
            first = "MIN"

    # See if its a relative max
    elif df["Price"][i] > df["Price"][i - 1] and df["Price"][i] > next_value:
        max_values["Second"].append(df['Second'][i])
        max_values["Price"].append(df["Price"][i])
        relative_max(max_values["Second"].index(i), first, min_values, max_values)

    # See if its a relative min
    elif df["Price"][i] < df["Price"][i - 1] and df["Price"][i] < next_value:
        min_values["Second"].append(df["Second"][i])
        min_values["Price"].append(df["Price"][i])
        relative_min(min_values["Second"].index(i), first, min_values, max_values)

    return


def plot_stock_graph(df, max_values, min_values):
    x = range(len(df["Price"]))
    # plot stock graph
    plt.plot(x, df["Price"], label='stock')
    plt.scatter(max_values["Second"], max_values["Price"], color='r')
    plt.scatter(min_values["Second"], min_values["Price"], color='b')
    plt.plot(x, df["Price"])
    plt.xlabel('Time')
    plt.ylabel('Price')
    return plt.show()

