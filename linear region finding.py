from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np
import sys

xsize = 200
ysize = 200
daysInfectious = 1
probability_of_infection = 0.9
lattice = np.zeros((xsize,ysize))
seedRow = int(xsize/2)
seedColumn = int(ysize/2)

# we only consider the biggest cluster so when the probability is above percolation probability we can initialise multiple nucleation points
# (so long as the number of nucleation points << number of lattice points) as the clusters connect to form a single cluster. This ensures that
# we are always considering the largest cluster.
if probability_of_infection < 0.593:
       lattice[seedRow][seedColumn] = 1
else:
       for i in range(0,xsize, int(xsize/10)):
              for ii in range(0,ysize, int(ysize/10)):
                     lattice[i][ii] = 1
                     
cmap = colors.ListedColormap(['green', 'red', 'black'])
bounds=[0, 1, daysInfectious + 1, daysInfectious + 2]
norm = colors.BoundaryNorm(bounds, cmap.N)
dead_value = daysInfectious
timestep = 0
cleanList = list()
deadList = list()
infectedList = list()

figure, (mapping, graph) = plt.subplots(1, 2)
image = mapping.imshow(lattice, origin='lower', cmap=cmap, norm=norm)

max_iterations = 220
running = True
prevInfected = 0
while running:
        figure.suptitle('Iteration ' + str(timestep))
        infected = 0
        clean = 0 
        dead = 0
        xcounter = 0
        ycounter = 0
       
        newInfected = list()
       
        running = False
        for x in lattice:
              ycounter = 0
              for y in x:
                      if y == 0:
                            clean += 1
                      elif y > 0 and y <= daysInfectious:
                            infected += 1
                            running = True
                                                               
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

        cleanList.append(clean)
        deadList.append(dead)
        infectedList.append(infected)
        graph.plot(cleanList, color='green', label='Uninfected')
        graph.plot(infectedList, color='red', label = 'Infected')
        graph.plot(deadList, color='black', label = 'Recovered')
      
        timestep += 1
        image.set_data(lattice)
        plt.draw()
        plt.pause(0.001)

# generally 45% of the grid size gives a good upper limit
max_box_size = int(0.3*xsize)
best_db = 0
lowest_variance = sys.maxsize
best_range = []

# calculates box dimension for all possible ranges of box size with a minimum number of points of 5
# -4 and + 4 to have at least 5 points for the linear fit. Keeps track of range with lowest variance
# on the box counting dimension.
for j in range(1, max_box_size - 4):
       for jj in range(max_box_size, j + 4, -1):
              print(str(j) + " " + str(jj))
              box_sizes = np.array(range(j,jj))
              box_values = np.zeros(len(box_sizes))
              xcounter = 0
              ycounter = 0
              side_position = 0
              has_dead = False
              for side in box_sizes:
                     for x in range(0, xsize, side):
                            for y in range(0, xsize, side):
                                   has_dead = False
                                   if x + side <= xsize and y + side <= xsize:
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
                     best_range = np.array(range(j, jj))

print(np.sqrt(lowest_variance))
print(best_db)
print(best_range)