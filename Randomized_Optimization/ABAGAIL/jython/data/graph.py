import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# ContinuousPeaks_GA

from numpy import genfromtxt
ContinuousPeaks_GA = genfromtxt('ContinuousPeaks_GA.csv', delimiter=',')


print ContinuousPeaks_GA