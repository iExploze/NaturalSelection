import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import numpy as np
import pandas as pd


path = 'logs/ian2.csv'


data = np.genfromtxt(path, delimiter=",", names=['generation', 'amount_creatures', 'average_energy', 'average_speed',
												 'average_sense', 'reproduced', 'survived', 'died'])

plot1 = plt.figure(1)
plt.plot(data['generation'], data['average_speed'], color='red')
plt.plot(data['generation'], data['average_sense'], color='blue')
plt.title('Genetic Drift')
plt.xlabel('Generations')
plt.ylabel('Genetic Multiplier')
plt.legend(['Avg. Speed', 'Avg. Sense'])
plt.grid()

# plt.scatter(data['average_speed'], data['average_sense'])

plot2 = plt.figure(2)
plt.plot(data['generation'], data['amount_creatures'], color='black')
plt.plot(data['generation'], data['reproduced'], color='lime', alpha=0.9)
plt.plot(data['generation'], data['survived'], color='blue', alpha=0.9)
plt.plot(data['generation'], data['died'], color='gray', alpha=0.9)
plt.plot(data['generation'], data['average_energy'], color='gold')
plt.title('Population Statistics')
plt.xlabel('Generations')
plt.ylabel('# Creatures | Average Energy')
plt.legend(['Total Population', 'Births', 'Survivors', 'Deaths', 'Avg. Creature Energy'])
plt.grid()



plt.show()
