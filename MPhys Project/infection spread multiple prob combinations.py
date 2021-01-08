#Produces contour plot of average final box dimension of percolation model for different probability combinations for travel and occuptation

from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np
from percolation import percolate, percolate_and_travel
from box_counting import box_count, box_count_linear_fit
from scipy.interpolate import griddata
from matplotlib import cm
import matplotlib.pylab as pylab

params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

xsize = 100
ysize = 100

travel_upper = 1
occupation_upper = 1

probability_of_occupation = np.linspace(0, occupation_upper, 101)
probability_of_travel = np.linspace(0, travel_upper, 101)
probability_of_recovery = 0
probability_of_death = 0

days_infectious = 1
immune_period = 0
dead_value = 2

lockdown_percentage_start = 1
lockdown_percentage_end = 0
lockdown_effectiveness = 1
lockdown = False

seedRow = int(xsize/2)#np.random.randint(0,xsize-1)
seedColumn = int(ysize/2)#np.random.randint(0,ysize-1)

box_dimension_list = list()
box_dim_var_list = list()

simulations = 10


for prob_occ in probability_of_occupation:
       print(prob_occ)
       box_dim_line = list()

       for prob_tr in probability_of_travel:
              print(prob_tr)
              box_dimension_average = 0
              for i in range(0, simulations):
              
                     running = True
                     lattice = np.zeros((xsize,ysize))
                     lattice[seedRow][seedColumn] = 1
                     while running:     
                            lattice, lockdown, running = percolate_and_travel(lattice, days_infectious, dead_value, prob_occ, prob_tr, probability_of_death, probability_of_recovery, immune_period, lockdown, lockdown_percentage_start, lockdown_percentage_end, lockdown_effectiveness)
                                 
                     box_dimension, box_dimension_variance = box_count_linear_fit(lattice, dead_value)
                     if box_dimension < 0:
                            box_dimension = 0
                     elif box_dimension > 2:
                            box_dimension = 2
                     box_dimension_average += box_dimension
              box_dimension_average = box_dimension_average / simulations
              box_dim_line.append(box_dimension_average)
       box_dimension_list.append(box_dim_line)
              
box_dimension_list = np.array(box_dimension_list)

fig, ax = plt.subplots()
cax = ax.imshow(box_dimension_list, interpolation='nearest', cmap=cm.coolwarm, origin='lower')
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_xticklabels([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
cbar = fig.colorbar(cax, ticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0])

