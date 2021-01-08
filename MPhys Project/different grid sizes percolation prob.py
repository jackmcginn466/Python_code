import matplotlib.pyplot as plt
import numpy as np

#Code produces a graph of occupation probability against percolation probability. Percolation probability is fraction of simulations that percolate for that occupation probability

daysInfectious = 1 # number of days an infectious person 
dead_value = daysInfectious
simulations = 100 # number of simulations for each probability

box_dimensions_list = list()
box_dimensions_uncertainty_list = list()
prob_list = np.linspace(0, 1, 101)
percolation_list = []
percolation_uncertainty_list = []
box_size_list = [10, 50, 100, 200]

g, ax = plt.subplots()
   
for size in box_size_list:
       for probability_of_infection in prob_list:  
              
              percolation_counter = 0.0 # keeps track of number of successful percolations for each probability of infection              
              print(probability_of_infection)
              
              for i in range(0, simulations):
                     seedRow = int(size/2) # start each infection at the middle of the lattice, arbitrary choice that reduces chance of hitting side of lattice 
                     seedColumn = int(size/2)
                     lattice = np.zeros((size,size)) # lattice starts as array of 0's where 0 indicates uninfected
                     lattice[seedRow][seedColumn] = 1 # one infectious person introduced
                     # for a in range(0, xsize, int(xsize/10)):
                     #        for b in range(0, ysize, int(ysize/10)): // initialise multiple nucleation points
                     #               lattice[a][b] = 1
                     running = True # is the current simulation still running
                     prevInfected = 0
                     
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
                     
                     percolated = False
                     
                     top_side = False
                     left_side = False
                     right_side = False
                     
                     # checks if simulation has percolated from left to right of grid and keep count of number of times percolated
                     for x in lattice:
                             if x[0] > 0:
                                   left_side = True
                             if x[-1] > 0:
                                   right_side = True
                             if left_side == True and right_side == True:
                                   percolation_counter += 1
                                   percolated = True
                                   break
                     # checks if simulation has percolated from top to bottom if it hasn't already percolated left to right and keeps track of
                     # number of times percolated
                     if percolated == False:
                             for x in lattice[0]:                           
                                   if x == 1:
                                           top_side = True
                             for x in lattice[-1]:
                                   if x == 1 and top_side == True:
                                           percolation_counter += 1
                                           percolated = True
                                           break
                     
              # percolation_counter/simulations gives the probability of percolation for each probability                     
              percolation_list.append(percolation_counter/simulations)
              percolation_uncertainty_list.append(np.sqrt((percolation_counter*(1 - percolation_counter/simulations)**2 + (simulations - percolation_counter)*(percolation_counter/simulations)**2)/((simulations - 1)*simulations)))
       
       ax.errorbar(prob_list, percolation_list, yerr=percolation_uncertainty_list, linestyle='None', fmt='o')                     
       percolation_list.clear()
       percolation_uncertainty_list.clear()                                   
ax.legend()
g.show()
