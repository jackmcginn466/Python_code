# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 16:06:29 2020
Code to crop images to remove excess whitespace and saves over previous images, performs box counting method on cropped images to find box dimension for each
and plots box dimension against date for the images. Image names input must be in the form ddmmyyyy
@author: Matt
"""
import cv2
import numpy as np
import os
from matplotlib import colors
import matplotlib.pyplot as plt
import sys
import datetime
import csv

cmap = colors.ListedColormap(['white', 'black']) # colours to use in colour map
bounds = [0, 1, 2] # bounds to determine colour that should be assigned from colour map
norm = colors.BoundaryNorm(bounds, cmap.N)

results = list()

for root, dirs, files in os.walk(os.getcwd()): # loops through files in current directory
       for name in files:
              if name.endswith(".png") or name.endswith(".PNG"):
                     print(name)
                     im = cv2.imread(name)
                     im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB) # convert image array to RGB from BGR
                     
                     vertCroppedIm = list() # list to store image when cropped at top and bottom
                     
                     # checks each line in the image to see if it contains a non-white pixel and stores it in vertCroppedIm if it does
                     for line in im:
                            keepLine = False
                            for pixel in line:
                                   if (pixel == [210, 212, 206]).all() or (pixel == [255, 0, 0]).all():
                                          keepLine = True
                                          break
                            if keepLine == True:      
                                   vertCroppedIm.append(line)
                     
                     endPoint = sys.maxsize
                     startPoint = sys.maxsize
                     
                     # find leftmost and rightmost column that contain a non-white pixel
                     for line in vertCroppedIm:
                            pixelNumberStart = 0
                            pixelNumberEnd = 0
                            for pixel in line:
                                   if (pixel == [210, 212, 206]).all() or (pixel == [255, 0, 0]).all():
                                          if pixelNumberStart < startPoint:
                                                 startPoint = pixelNumberStart
                                          break
                                   pixelNumberStart += 1
                            for pixel in reversed(line):
                                   if (pixel == [210, 212, 206]).all() or (pixel == [255, 0, 0]).all():
                                          if pixelNumberEnd < endPoint:
                                                 endPoint = pixelNumberEnd
                                          break
                                   pixelNumberEnd += 1
                     
                     endPoint = endPoint + 1 # add one to endPoint as when measuring backwards in array these values start at 1, not 0
                     croppedIm = list() 
                     
                     for line in vertCroppedIm:
                            croppedIm.append(line[startPoint:-endPoint])
                     
                     croppedIm = np.array(croppedIm)
                     croppedIm = cv2.cvtColor(croppedIm, cv2.COLOR_RGB2BGR) # convert back to BGR from RGB to write to file
                     cv2.imwrite(name, croppedIm)
                     croppedIm = cv2.cvtColor(croppedIm, cv2.COLOR_BGR2RGB) # convert back to RGB for further analysis
                     
                     lattice = list()
                     # turn image into a lattice of 1s (if pixel red) and 0s (if pixel white or gray)
                     for line in croppedIm:
                            lattice.append([0 if ((np.array_equal(pixel, np.array([255, 255, 255]))) or (np.array_equal(pixel, np.array([210, 212, 206])))) else 1 for pixel in line])
                     
                     xsize = len(lattice)
                     ysize = len(lattice[0]) 
                     
                     box_sizes = np.array(range(1, 20)) # linear range of graph for box counting method
                     box_values = np.zeros(len(box_sizes))
                     
                     xcounter = 0
                     ycounter = 0
                     side_position = 0
                     has_infected = False
                     # loops through side lengths in box sizes and counts number of boxes of that size containing an infected (array element = 1) in the lattice
                     for side in box_sizes:
                            for x in range(0, xsize, side):
                                   for y in range(0, ysize, side):
                                          has_dead = False
                                          if x + side <= xsize and y + side <= ysize:
                                                 for i in range(0, side):
                                                        for ii in range(0, side):
                                                               if lattice[x + i][y + ii] == 1:
                                                                      has_infected = True
                                          if has_infected == True:
                                                 box_values[side_position] += 1
                            side_position += 1
                     # calculate linear fit as per usual box counting method with covariance to find uncertainties and append to results
                     coeffs, cov = np.polyfit(np.log(1/box_sizes), np.log(box_values), 1, cov=True, full=False)               
                     results.append([name, coeffs[0], np.sqrt(np.diag(cov)[0])])
                     
dates = list()
boxDim = list()
boxDimError = list()

# convert dates to a datetime object which numpy and matplotlib use to plot dates
dates = [datetime.datetime.strptime((line[0])[:-4], '%d%m%Y').date() for line in results]

for line in results:
       boxDim.append(float(line[1]))
       boxDimError.append(float(line[2]))
       
dates = np.array(dates)
boxDim = np.array(boxDim)
boxDimError = np.array(boxDimError)

fig, ax1 = plt.subplots()

ax1.errorbar(dates, boxDim, yerr=boxDimError, linestyle='None', color = 'tab:blue', fmt = 'o') # error bars on points
ax1.set_xlabel('Date')
ax1.set_ylabel('Box dimension', color='tab:blue')

dates = list()
infected = list()

# read in new cases per day from csv file and store in arrays to be plotted
with open('new cases per day.csv') as csv_file:
       csv_reader = csv.reader(csv_file, delimiter=',')
       for row in csv_reader:
            dates.append(row[0])
            infected.append(int(row[1]))
       weeklydates = dates[0::7]

# calculate weekly infected from previous arrays
infectedWeekly = []
for x in range(0, len(infected), 7):
    infectedWeekly.append(sum(infected[x:x+7])/7)

weeklydates = [datetime.datetime.strptime(line, '%d/%m/%Y').date() for line in weeklydates]
weeklydates = np.array(weeklydates)
infectedWeekly = np.array(infectedWeekly)
         
dates = [datetime.datetime.strptime(line, '%d/%m/%Y').date() for line in dates]
dates = np.array(dates)
infected = np.array(infected)

ax2 = ax1.twinx()

ax2.plot(weeklydates, infectedWeekly, color='tab:red')
ax2.set_ylabel('New infected', color='tab:red')

fig.tight_layout()

plt.show()    