# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 17:28:10 2020

@author: Matt
"""
import numpy as np

def percolate(lattice, days_infectious = 1, dead_value = 2, probability_of_occupation = 0, probability_of_death = 0, probability_of_recovery = 0, immune_period = 0, lockdown = False, lockdown_percentage_start = 1, lockdown_percentage_end = 0, lockdown_effectiveness = 1):
       size = len(lattice)
       infected = 0
       clean = 0 
       dead = 0
       x_counter = 0
       y_counter = 0
       
       new_infected = list()
       
       running = False
       
       for x in lattice:
              y_counter = 0
              for y in x:
                     if y == 0:
                            clean += 1
                     elif y == dead_value:
                            dead += 1
                     elif y > 0 and y <= days_infectious:
                            infected += 1
                            running = True
                            lattice[x_counter][y_counter] += 1
                            if np.random.uniform(0, 1) < probability_of_death: # if person dies
                                   lattice[x_counter][y_counter] = dead_value # set to dead value
                            else:                                                 
                                   if y_counter < size - 1:
                                          if lattice[x_counter][y_counter + 1] == 0:
                                                 right = np.random.uniform(0,1)
                                                 if right < probability_of_occupation:
                                                        new_infected.append((x_counter, y_counter + 1))
                                                 else:
                                                        lattice[x_counter][y_counter + 1] = -1
                                   if y_counter > 0:
                                          if lattice[x_counter][y_counter - 1] == 0:
                                                 left = np.random.uniform(0,1)
                                                 if left < probability_of_occupation:
                                                        new_infected.append((x_counter, y_counter - 1))
                                                 else:
                                                        lattice[x_counter][y_counter - 1] = -1                                                        
                                   if x_counter < size - 1:
                                          if lattice[x_counter + 1][y_counter] == 0:
                                                 up = np.random.uniform(0,1)
                                                 if up < probability_of_occupation:
                                                        new_infected.append((x_counter + 1, y_counter))   
                                                 else:
                                                        lattice[x_counter + 1][y_counter] = -1                                                        
                                   if x_counter > 0:
                                          if lattice[x_counter - 1][y_counter] == 0:
                                                 down = np.random.uniform(0,1)
                                                 if down < probability_of_occupation:
                                                        new_infected.append((x_counter - 1, y_counter))   
                                                 else:
                                                        lattice[x_counter - 1][y_counter] = -1                                                        
                                   
                     elif y == days_infectious + 1:
                            rand = np.random.uniform(0, 1)
                            if rand < probability_of_recovery:
                                   lattice[x_counter][y_counter] = -immune_period
                                   clean += 1
                            else: 
                                   dead += 1
                                   lattice[x_counter][y_counter] = dead_value 
                     y_counter += 1    
              x_counter += 1
       for ill in new_infected:
              lattice[ill[0]][ill[1]] = 1
       if clean + infected != 0:
              if infected / (clean + infected) > lockdown_percentage_start and lockdown == False:
                     lockdown = True
                     probability_of_occupation = probability_of_occupation / lockdown_effectiveness
              elif lockdown == True and infected / (clean + infected) < lockdown_percentage_end:
                     probability_of_occupation = probability_of_occupation * lockdown_effectiveness
                     lockdown = False
       return lattice, lockdown, running

def percolate_and_travel(lattice, days_infectious = 1, dead_value = 2, probability_of_occupation = 0, probability_of_travel = 0, probability_of_death = 0, probability_of_recovery = 0,  immune_period = 0, lockdown = False, lockdown_percentage_start = 1, lockdown_percentage_end = 0, lockdown_effectiveness = 1):
       size = len(lattice)
       infected = 0
       clean = 0 
       dead = 0
       x_counter = 0
       y_counter = 0
       
       new_infected = list()
       
       running = False
       
       for x in lattice:
              y_counter = 0
              for y in x:
                     if y == 0:
                            clean += 1
                     elif y == dead_value:
                            dead += 1
                     elif y > 0 and y <= days_infectious:
                            remaining_clean = size*size - np.sum(np.abs(lattice))
                            if np.random.uniform(0, 1) < probability_of_travel and remaining_clean > 0:
                                  # travelled = False
                                  # while not travelled:    
                                   randx = int(np.random.uniform(0, size-1))
                                   randy = int(np.random.uniform(0, size-1))
                                   if lattice[randx][randy] == 0:
                                                 #travelled = True
                                                 new_infected.append((randx, randy))                                   
                                                 infected += 1
                            
                            infected += 1
                            running = True
                            lattice[x_counter][y_counter] += 1
                            if np.random.uniform(0, 1) < probability_of_death: # if person dies
                                   lattice[x_counter][y_counter] = dead_value # set to dead value
                            else:                                                 
                                   if y_counter < size - 1:
                                          if lattice[x_counter][y_counter + 1] == 0:
                                                 right = np.random.uniform(0,1)
                                                 if right < probability_of_occupation:
                                                        new_infected.append((x_counter, y_counter + 1))
                                                 else:
                                                        lattice[x_counter][y_counter + 1] = -1
                                   if y_counter > 0:
                                          if lattice[x_counter][y_counter - 1] == 0:
                                                 left = np.random.uniform(0,1)
                                                 if left < probability_of_occupation:
                                                        new_infected.append((x_counter, y_counter - 1))
                                                 else:
                                                        lattice[x_counter][y_counter - 1] = -1                                                        
                                   if x_counter < size - 1:
                                          if lattice[x_counter + 1][y_counter] == 0:
                                                 up = np.random.uniform(0,1)
                                                 if up < probability_of_occupation:
                                                        new_infected.append((x_counter + 1, y_counter))   
                                                 else:
                                                        lattice[x_counter + 1][y_counter] = -1                                                        
                                   if x_counter > 0:
                                          if lattice[x_counter - 1][y_counter] == 0:
                                                 down = np.random.uniform(0,1)
                                                 if down < probability_of_occupation:
                                                        new_infected.append((x_counter - 1, y_counter))   
                                                 else:
                                                        lattice[x_counter - 1][y_counter] = -1                                                        
                                   
                     elif y == days_infectious + 1:
                            rand = np.random.uniform(0, 1)
                            if rand < probability_of_recovery:
                                   lattice[x_counter][y_counter] = -immune_period
                                   clean += 1
                            else: 
                                   dead += 1
                                   lattice[x_counter][y_counter] = dead_value 
                     y_counter += 1    
              x_counter += 1
       for ill in new_infected:
              lattice[ill[0]][ill[1]] = 1
       if clean + infected != 0:
              if infected / (clean + infected) > lockdown_percentage_start and lockdown == False:
                     lockdown = True
                     probability_of_occupation = probability_of_occupation / lockdown_effectiveness
              elif lockdown == True and infected / (clean + infected) < lockdown_percentage_end:
                     probability_of_occupation = probability_of_occupation * lockdown_effectiveness
                     lockdown = False
       return lattice, lockdown, running