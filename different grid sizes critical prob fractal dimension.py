import matplotlib.pyplot as plt
import numpy as np
import sys

daysInfectious = 1 # number of days an infectious person 
dead_value = daysInfectious
simulations = 20 # number of simulations for each probability

box_dimensions_list = list()
box_dimensions_uncertainty_list = list()
probability_of_infection = 0.593
percolation_list = []
percolation_uncertainty_list = []
grid_size_list = np.linspace(50, 500, 19, dtype=int)

for size in grid_size_list:
       print(size)
       fractalDim = 0
       fractalDimUncertainty = 0
       for i in range(0, simulations):
              lattice = np.zeros((size,size)) # lattice starts as array of 0's where 0 indicates uninfected
              running = True # is the current simulation still running
              prevInfected = 0
              
              if int(0.005 * size**2) == 0:
                     lattice[int(size/2)][int(size/2)] = 1
              else:
                     number_of_nucleation_points = int(0.005 * size**2)              
                     for x in range(0, size, int(size/np.sqrt(number_of_nucleation_points))):
                             for y in range(0, size, int(size/np.sqrt(number_of_nucleation_points))):                               
                                    lattice[x][y] = 1 # infectious person introduced

              
              while running:
                     running = False
                     infected = 0
                     xcounter = 0 # x position in lattice
                     ycounter = 0 # y position in lattice
                     newInfected = list() # list used to add infected to lattice after a timestep
                     # loops through lattice to find infectious points in lattice and check to see if adjacent points are made infectious
                     # daysInfectious used here as we also use this in the model. daysInfectious = 1 is equivalent of standard percolation
                     # add any new infected points to a list to be added to the lattice after we have checked the entire lattice
                     for x in lattice:
                            ycounter = 0
                            for y in x:
                                    if y > 0 and y <= daysInfectious:
                                          running = True
                                          infected += 1                                        
                                          if ycounter < size - 1:
                                                  if lattice[xcounter][ycounter + 1] == 0:
                                                        right = np.random.uniform(0,1)
                                                        if right < probability_of_infection:
                                                                newInfected.append((xcounter, ycounter + 1))
                                                        else:
                                                                lattice[xcounter][ycounter + 1] = -1
                                          if ycounter > 0:
                                                  if lattice[xcounter][ycounter - 1] == 0:
                                                        left = np.random.uniform(0,1)
                                                        if left < probability_of_infection:
                                                                newInfected.append((xcounter, ycounter - 1))
                                                        else:
                                                                lattice[xcounter][ycounter - 1] = -1                                                        
                                          if xcounter < size - 1:
                                                  if lattice[xcounter + 1][ycounter] == 0:
                                                        up = np.random.uniform(0,1)
                                                        if up < probability_of_infection:
                                                                newInfected.append((xcounter + 1, ycounter))   
                                                        else:
                                                                lattice[xcounter + 1][ycounter] = -1                                                        
                                          if xcounter > 0:
                                                  if lattice[xcounter - 1][ycounter] == 0:
                                                        down = np.random.uniform(0,1)
                                                        if down < probability_of_infection:
                                                                newInfected.append((xcounter - 1, ycounter))   
                                                        else:
                                                                lattice[xcounter - 1][ycounter] = -1                                                                                    
                                    ycounter += 1    
                            xcounter += 1
                     if prevInfected == infected:
                            running = False
                     else:
                            prevInfected = infected
                     for ill in newInfected:
                            lattice[ill[0]][ill[1]] = 1
              ##############################################################
              
             
              
              if size <= 50:
                     # generally 45% of the grid size gives a good upper limit
                     max_box_size = int(size/2)
                     best_db = 0
                     lowest_variance = sys.maxsize
                     best_range = []
                     # calculates box dimension for all possible ranges of box size with a minimum number of points of 5
                     # -4 and + 4 to have at least 5 points for the linear fit. Keeps track of range with lowest variance
                     # on the box counting dimension.
                     for j in range(3, max_box_size):
                            box_sizes = np.array(range(1, j + 1))
                            box_values = np.zeros(len(box_sizes))
                            xcounter = 0
                            ycounter = 0
                            side_position = 0
                            has_dead = False
                            for side in box_sizes:
                                   for x in range(0, size, side):
                                          for y in range(0, size, side):
                                                 has_dead = False
                                                 if x + side <= size and y + side <= size:
                                                        for i in range(0, side):
                                                               for ii in range(0, side):
                                                                      if lattice[x + i][y + ii] == dead_value:
                                                                             has_dead = True
                                                 if has_dead == True:
                                                        box_values[side_position] += 1
                                   side_position += 1
                            coeffs, cov = np.polyfit(np.log(1/box_sizes), np.log(box_values), 1, cov=True, full=False) # best fit line through points to estimate fractal dimension
                            
                            if np.diag(cov)[0] < lowest_variance and coeffs[0] > 1:
                                   lowest_variance = np.diag(cov)[0]
                                   best_db = coeffs[0]
                                   best_range = np.array(range(1, j))
                     print(best_range)                     
                     
              else:       
                     
                     # generally 45% of the grid size gives a good upper limit
                     max_box_size = int(16)
                     best_db = 0
                     lowest_variance = sys.maxsize
                     best_range = []
                     # calculates box dimension for all possible ranges of box size with a minimum number of points of 5
                     # -4 and + 4 to have at least 5 points for the linear fit. Keeps track of range with lowest variance
                     # on the box counting dimension.
                     for j in range(7, max_box_size):
                            box_sizes = np.array(range(2, j + 1))
                            box_values = np.zeros(len(box_sizes))
                            xcounter = 0
                            ycounter = 0
                            side_position = 0
                            has_dead = False
                            for side in box_sizes:
                                   for x in range(0, size, side):
                                          for y in range(0, size, side):
                                                 has_dead = False
                                                 if x + side <= size and y + side <= size:
                                                        for i in range(0, side):
                                                               for ii in range(0, side):
                                                                      if lattice[x + i][y + ii] == dead_value:
                                                                             has_dead = True
                                                 if has_dead == True:
                                                        box_values[side_position] += 1
                                   side_position += 1
                            coeffs, cov = np.polyfit(np.log(1/box_sizes), np.log(box_values), 1, cov=True, full=False) # best fit line through points to estimate fractal dimension
                            
                            if np.diag(cov)[0] < lowest_variance and coeffs[0] > 1:
                                   lowest_variance = np.diag(cov)[0]
                                   best_db = coeffs[0]
                                   best_range = np.array(range(2, j))
                     print(best_range)                     
              fractalDim += (1/lowest_variance)*best_db
              fractalDimUncertainty += 1/lowest_variance 
       fractalDim = fractalDim / fractalDimUncertainty
       fractalDimUncertainty = np.sqrt(1/fractalDimUncertainty)
       box_dimensions_list.append(fractalDim)
       box_dimensions_uncertainty_list.append(fractalDimUncertainty)
f, ax = plt.subplots()
ax.set_ylim([0, 2])
ax.errorbar(grid_size_list, box_dimensions_list, yerr=box_dimensions_uncertainty_list, linestyle='None', fmt='o')            
f.show()                         