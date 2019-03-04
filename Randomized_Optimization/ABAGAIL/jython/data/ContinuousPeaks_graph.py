import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy import genfromtxt

# ContinuousPeaks_GA
ContinuousPeaks_GA = genfromtxt('ContinuousPeaks_GA.csv', delimiter=',')

# ContinuousPeaks_MIMIC
ContinuousPeaks_MIMIC = genfromtxt('ContinuousPeaks_MIMIC.csv', delimiter=',')

# ContinuousPeaks_RHC
ContinuousPeaks_RHC = genfromtxt('ContinuousPeaks_RHC.csv', delimiter=',')

# ContinuousPeaks_SA
ContinuousPeaks_SA = genfromtxt('ContinuousPeaks_SA.csv', delimiter=',')

# Data structure-> [T, iterations, fitness, time]


T = ContinuousPeaks_SA[:, 0]
iterations = ContinuousPeaks_SA[:, 1]



fitness_GA = ContinuousPeaks_GA[:, 2]
fitness_MIMIC = ContinuousPeaks_MIMIC[:, 2]
fitness_RHC = ContinuousPeaks_RHC[:, 2]
fitness_SA = ContinuousPeaks_SA[:, 2]

# plt.plot(iterations, fitness_GA)
# plt.plot(iterations, fitness_MIMIC)
# plt.plot(iterations, fitness_RHC)
plt.plot(iterations, fitness_SA)




# ax = plt.axes(projection='3d')
# ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none');

# ax.set_xlabel('Iterations')
# ax.set_ylabel('T')
# ax.set_zlabel('fitness_GA')
# ax.set_title('Fitness SA\ntemperature = 1E11, cooling rate = 0.95')

plt.show()

