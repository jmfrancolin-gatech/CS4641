import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy import genfromtxt

# ContinuousPeaks_MIMIC
data = genfromtxt('TravelingSalesman_GA.csv', delimiter=',')



Points = data[:, 0]
iterations = data[:, 1]
fitness_MIMIC = data[:, 2]
time_MIMIC = data[:, 3]






ax = plt.axes(projection='3d')
ax.plot_trisurf(iterations, Points, time_MIMIC, cmap='viridis', edgecolor='none');

ax.set_xlabel('Iterations')
ax.set_ylabel('Time')
ax.set_zlabel('Fitness')
ax.set_title('Fitness GA')

plt.show()

