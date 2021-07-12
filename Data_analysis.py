#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 08:32:47 2020

@author: Mathew
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import os


# The thresholds and filenames etc. need to be placed below

path_sample = r"/Users/Mathew/Documents/Current analysis/20210610_3h_5nMAb_5uMThT/"           # This is the folder that contains the dye + sample
file_stem_sample="AbThT"   


# Set the various thresholds here

threshold_small=20
threshold_medium=30
threshold_large=500



def load_files_sample(filename_contains):
    num=0
    channelA_sample=[]             # Where channel A data will be stored
    channelB_sample=[]             # Where channel B data will be stored
    for root, dirs, files in os.walk(path_sample):
      for name in files:
              if filename_contains in name:
                  resultsname = name
                  print(name)
                  num+=1
                  a=0
                  with open(resultsname) as csvDataFile:                                                # Opens the file as a CSV
                        csvReader = csv.reader(csvDataFile,delimiter='\t')                           # Assigns the loaded CSV file to csvReader. 
                        for row in csvReader:
                            channelA_sample.append(row[0])                                                     # For every row in in csvReader, the values are apended to green and red.         
                            channelB_sample.append(row[1])
                            a+=1
        
                            print ("Loaded %s, which contains %s rows."%(resultsname,a))
        
    print("Loaded %s files in total"%num)
        
    channelA_arr_sample=np.asarray(channelA_sample,dtype=np.float32)                              # Converts these to numpy arrays for vector calcs.
    channelB_arr_sample=np.asarray(channelB_sample,dtype=np.float32)
    return channelA_arr_sample,channelB_arr_sample


def intensity_separate(input_file):
    small_events=input_file[np.logical_and(input_file>threshold_small, input_file<threshold_medium)] 
    medium_events=input_file[np.logical_and(input_file>threshold_medium, input_file<threshold_large)] 
    all_events=input_file[(input_file>threshold_small)]
    large_events=input_file[(input_file>threshold_large)]                 
    return all_events,small_events,medium_events,large_events

channelA_arr_sample,channelB_arr_sample=load_files_sample(file_stem_sample)

 
plt.plot(channelA_arr_sample)
plt.xlim(0,500000)
plt.ylim(0,50)
plt.xlabel('Bin number')
plt.ylabel('Intensity (photons)')
plt.savefig(path_sample+'Raw.pdf')
plt.show()    

all_events,small_events,medium_events,large_events=intensity_separate(channelA_arr_sample)


plt.hist(all_events,bins = 50,range=[threshold_small,1000], rwidth=0.9,color='#ff0000')
plt.xlabel('Intensity (photons)',size=20)
plt.yscale('log')
plt.ylabel('Number of Events',size=20)
plt.savefig(path_sample+"Intensities.pdf")
plt.show()

total_events=len(all_events)
total_small=len(small_events)
total_medium=len(medium_events)
total_large=len(large_events)

print('All events: %d \nSmall events: %d\nMedium events: %d\nLarge events: %d'%(total_events,total_small,total_medium,total_large))
