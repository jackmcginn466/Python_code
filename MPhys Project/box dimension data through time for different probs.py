#Calculates box dimension of fractals at each iteration of the percolation proccess for each probability combination for percolation and then saves all this data to a csv

import numpy as np
from percolation import percolate, percolate_and_travel
from box_counting import box_count, box_count_linear_fit

xsize = 250
ysize = 250
days_infectious = 1

occupation_upper = 1
travel_upper = 1

probability_of_occupation = np.linspace(0.04, occupation_upper, 97)
probability_of_travel = np.linspace(0, travel_upper, 101)
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

lockdown = False
running = True
max_timesteps = 37
simulations = 10
box_dim_list = list()
box_dim_var_list = list()

#overall_list = ["prob_occ", "prob_travel", "box_dimension each time step"]
overall_list = list()

for prob_occ in probability_of_occupation:
       print(prob_occ)

       for prob_travel in probability_of_travel:
              print(prob_travel)
              if prob_travel > 0.5 - 0.5*prob_occ: 
                     box_dim_average_list = np.zeros(max_timesteps - 1) # because we remove first value from this array as it is always zero
                     #counter = 0
                     for i in range(0, simulations):# and counter < simulations:
                            box_dim_list = np.zeros(max_timesteps)
                            running = True
                            lattice = np.zeros((xsize,ysize))
                            lattice[seedRow][seedColumn] = 1
                            counter = 0
                            while running and counter < max_timesteps:                              
                                   lattice, lockdown, running = percolate_and_travel(lattice, days_infectious, dead_value, prob_occ, prob_travel, probability_of_death, probability_of_recovery, immune_period, lockdown, lockdown_percentage_start, lockdown_percentage_end, lockdown_effectiveness)
                                  
                                   box_dimension, box_dimension_variance = box_count_linear_fit(lattice, dead_value)
                                   box_dim_list[counter] = box_dimension
                                   #box_count_linear_fit(lattice, dead_value)
                                   counter += 1
                            box_dim_list = box_dim_list[1:]
                            box_dim_list[box_dim_list == 0] = box_dim_list.max()
                            box_dim_average_list += np.array(box_dim_list)
                            counter += 1
                     
                     box_dim_average_list = box_dim_average_list / simulations
       
                     box_dim_average_list = np.insert(box_dim_average_list, 0, prob_travel)
                     box_dim_average_list = np.insert(box_dim_average_list, 0, prob_occ)
                     
                     overall_list.append(box_dim_average_list)
              else:
                     null_list = np.zeros(max_timesteps - 1)
                     null_list = np.insert(null_list, 0, prob_travel)
                     null_list = np.insert(null_list, 0, prob_occ)
                     overall_list.append(null_list)
                     
              
              
np.savetxt("data.csv", overall_list, delimiter=",")
