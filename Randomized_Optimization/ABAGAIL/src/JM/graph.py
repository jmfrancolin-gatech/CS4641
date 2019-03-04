import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# ContinuousPeaks_GA

from numpy import genfromtxt
my_data = genfromtxt('my_file.csv', delimiter=',')


ContinuousPeaks_GA = np.array([20,10000,20.0,0.674767743],
                            [100,30000,100.0,2.87022727])


            # [20,20000,20.0,1.012942427],
            # [20,30000,20.0,1.38817094],
            # [50,10000,50.0,0.687653134],
            # [50,20000,50.0,1.341964523],
            # [50,30000,50.0,2.73146043],
            # [100,10000,85.0,1.352759206],
            # [100,20000,100.0,1.746757478],
            # [100,30000,100.0,2.87022727])


print ContinuousPeaks_GA