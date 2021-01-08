# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 17:20:06 2020
"""
#Calculates box dimension of fractals in our lattice structures 

import numpy as np
import sys
import matplotlib.pyplot as plt
def box_count(lattice, box_range, dead_value):
       box_sizes = np.array(box_range)
       box_values = np.zeros(len(box_sizes))
       side_position = 0
       has_dead = False
       for side in box_sizes:
              for x in range(0, len(lattice), side):
                     for y in range(0, len(lattice[0]), side):
                            has_dead = False
                            if x + side <= len(lattice) and y + side <= len(lattice[0]):
                                   for i in range(0, side):
                                          for ii in range(0, side):
                                                 if lattice[x + i][y + ii] == dead_value:
                                                        has_dead = True
                            if has_dead == True:
                                   box_values[side_position] += 1
              side_position += 1
       coeffs, cov = np.polyfit(np.log(1/box_sizes), np.log(box_values), 1, cov=True, full=False) # best fit line through points to estimate fractal dimension
       return coeffs[0], np.diag(cov)[0]

def box_count_linear_fit(lattice, dead_value):
       best_box_dimension = 0.0
       lowest_variance = sys.maxsize
       xsize = len(lattice)
       ysize = len(lattice[0])
       
       if xsize < ysize:
              max_box_size = int(0.1*xsize) # change factor depending on size of images, will take way too long for e.g. a 500x500 lattice with 0.3
       else:
              max_box_size = int(0.1*ysize)
#       best_range = []
       
       # calculates box dimension for all possible ranges of box size with a minimum number of points of 5
       # Keeps track of range with lowest variance on the box counting dimension.
       for j in range(6, max_box_size):
              box_sizes = np.array(range(2, j + 1))
              box_values = np.zeros(len(box_sizes))
              side_position = 0
              has_dead = False
              for side in box_sizes:
                     for x in range(0, xsize, side):
                            for y in range(0, ysize, side):
                                   has_dead = False
                                   if x + side <= xsize and y + side <= ysize:
                                          for i in range(0, side):
                                                 for ii in range(0, side):
                                                        if lattice[x + i][y + ii] == dead_value:
                                                               has_dead = True
                                   if has_dead == True:
                                          box_values[side_position] += 1
                     side_position += 1
              coeffs, cov = np.polyfit(np.log(1/box_sizes), np.log(box_values), 1, cov=True, full=False) # best fit line through points to estimate fractal dimension
              if np.diag(cov)[0] < lowest_variance:
                     lowest_variance = np.diag(cov)[0]
                     best_box_dimension = coeffs[0]
              #                            best_range = np.array(range(2, jj))
       
       return best_box_dimension, lowest_variance
