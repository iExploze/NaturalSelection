import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import numpy as np
import pandas as pd


path = 'logs/conformity.csv'


data = np.genfromtxt(path, delimiter=",", names=['generation', 'amount_creatures', 'average_energy', 'average_speed', 'average_sense'])

plot1 = plt.figure(1)
plt.plot(data['generation'], data['average_speed'], color='red')
plt.plot(data['generation'], data['average_sense'], color='blue')
# plt.scatter(data['average_speed'], data['average_sense'])

plot2 = plt.figure(2)
plt.plot(data['generation'], data['average_energy'], color='gold')


plt.figure(3)
plt.plot(data['generation'], data['amount_creatures'], color='purple')


plt.show()
plt.show()