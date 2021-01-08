#Code runs and visualises a simple percolation proccess

from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np
from percolation import percolate, percolate_and_travel
from box_counting import box_count, box_count_linear_fit

xsize = 100
ysize = 100
days_infectious = 1
probability_of_occupation = 0.6
probability_of_travel = 0
probability_of_recovery = 0
probability_of_death = 0
immune_period = 0
lockdown_percentage_start = 1
lockdown_percentage_end = 0
lockdown_effectiveness = 1
lattice = np.zeros((xsize,ysize))
seedRow = int(xsize/2)#np.random.randint(0,xsize-1)
seedColumn = int(ysize/2)#np.random.randint(0,ysize-1)
dead_value = 2


lattice[seedRow][seedColumn] = 1
timestep = 0

cmap = colors.ListedColormap(['green', 'red'])
bounds=[ 0, 1, dead_value]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, mapping = plt.subplots()
image = mapping.imshow(lattice, origin='lower', cmap=cmap, norm=norm)

lockdown = False
running = True

box_dim_list = list()
box_dim_var_list = list()

while running:            
       lattice, lockdown, running = percolate_and_travel(lattice, days_infectious, dead_value, probability_of_occupation, probability_of_travel, probability_of_death, probability_of_recovery, immune_period, lockdown, lockdown_percentage_start, lockdown_percentage_end, lockdown_effectiveness)
      
   
       image.set_data(lattice)
       plt.draw()
       plt.pause(0.001)
       box_dimension, box_dimension_variance = box_count(lattice, np.array(range(2,10)), dead_value)
       box_dim_list.append(box_dimension)
       box_dim_var_list.append(box_dimension_variance)

box_dim_list = np.array(box_dim_list)
box_dim_var_list = np.array(box_dim_var_list)

fig, ax1 = plt.subplots()
print(box_dim_list[-1])
print(np.sqrt(box_dim_var_list[-1]))
ax1.errorbar(range(0, len(box_dim_list)), box_dim_list, yerr=np.sqrt(box_dim_var_list), linestyle='None', color = 'tab:blue', fmt = 'o') # error bars on points
ax1.set_xlabel('Date')
ax1.set_ylabel('Box dimension', color='tab:blue')
plt.show()
print("Box dimension = " + str(box_dimension) + " +/- " + str(np.sqrt(box_dimension_variance)))
