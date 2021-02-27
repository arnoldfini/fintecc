import pandas as pd
from matplotlib import pyplot as plt

f = pd.read_csv("Bitcoin Historical Data - Investing.com.csv")
price = f['Price']
print(f)
x = [i for i in range(len(f)-1, 0-1, -1)]

plt.plot(x, price)
plt.xlabel('Time')
plt.ylabel('Price')
plt.show()