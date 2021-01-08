import matplotlib.pyplot as plt
import numpy as np

xsize = 100 # x dimension of lattice
ysize = 100 # y dimension of lattice
daysInfectious = 1 # number of days an infectious person 
dead_value = daysInfectious
simulations = 100 # number of simulations for each probability
box_dimension = 0.0 
box_dimension_uncertainty = 0.0

box_dimensions_list = list()
box_dimensions_uncertainty_list = list()
prob_list = np.linspace(0, 1, 101)
percolation_list = []
percolation_uncertainty_list = []

for probability_of_infection in prob_list:  
       
       percolation_counter = 0.0      
       
       print(probability_of_infection)
       for i in range(0, simulations):
              seedRow = int(xsize/2) # start each infection at the middle of the lattice, arbitrary choice that reduces chance of hitting side of lattice 
              seedColumn = int(ysize/2)
              lattice = np.zeros((xsize,ysize)) # lattice starts as array of 0's where 0 indicates uninfected
              lattice[seedRow][seedColumn] = 1 # one infectious person introduced
              running = True # is the current simulation still running
              prevInfected = 0
              
              while running:
                     running = False
                     infected = 0
                     xcounter = 0 # x position in lattice
                     ycounter = 0 # y position in lattice
                     newInfected = list() # list used to add infected to lattice after a timestep
                     for x in lattice:
                            ycounter = 0
                            for y in x:
                                    if y > 0 and y <= daysInfectious:
                                          running = True
                                          #lattice[xcounter][ycounter] += 1
                                          infected += 1                                        
                                          if ycounter < ysize - 1:
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
                                          if xcounter < xsize - 1:
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

              percolated = False
              
              top_side = False
              left_side = False
              right_side = False

              for x in lattice:
                      if x[0] > 0:
                            left_side = True
                      if x[-1] > 0:
                            right_side = True
                      if left_side == True and right_side == True:
                            percolation_counter += 1
                            percolated = True
                            break
              if percolated == False:
                      for x in lattice[0]:                           
                            if x == 1:
                                    top_side = True
                      for x in lattice[-1]:
                            if x == 1 and top_side == True:
                                    percolation_counter += 1
                                    percolated = True
                                    break
              
                            
       percolation_list.append(percolation_counter/simulations)
       percolation_uncertainty_list.append(np.sqrt((percolation_counter*(1 - percolation_counter/simulations)**2 + (simulations - percolation_counter)*(percolation_counter/simulations)**2)/((simulations - 1)*simulations)))
      
       box_dimension = box_dimension / simulations # mean value of all simulations
       box_dimension_uncertainty = np.sqrt(box_dimension_uncertainty / (simulations - 1)) # standard deviation in the mean
       
       box_dimensions_list.append(box_dimension)
       box_dimensions_uncertainty_list.append(box_dimension_uncertainty)

plt.scatter(prob_list, percolation_list)
plt.errorbar(prob_list, percolation_list, yerr=percolation_uncertainty_list, linestyle='None')
plt.show()
