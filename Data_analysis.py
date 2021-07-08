#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 08:32:47 2020

@author: Mathew
"""

import numpy as np
import matplotlib.pyplot as plt
import csv



# The thresholds and filenames etc. need to be placed below

path_sample = r"/Users/Mathew/Documents/Current analysis/20210610_3h_5nMAb_5uMThT/"           # This is the folder that contains the dye + sample
file_stem_sample="AbThT"   



number_of_files=5       # Number of files in the folder (could make this automatic in the future).

# Set the various thresholds here

threshold_small=40
threshold_medium=500
threshold_large=1000



def load_files_sample(number_of_files):
    
    channelA_sample=[]             # Where channel A data will be stored
    channelB_sample=[]             # Where channel B data will be stored
    for i in range(0,number_of_files):
        
        if(i<1):
            filename=path_sample+file_stem_sample
        elif(i<10):
            filename=path_sample+file_stem_sample+"_0"+str(i+1)
        else:
            filename=path_sample+file_stem_sample+"_"+str(i+1)
        a=0                                                                             # Row counter
        with open(filename) as csvDataFile:                                                # Opens the file as a CSV
            csvReader = csv.reader(csvDataFile,delimiter='\t')                           # Assigns the loaded CSV file to csvReader. 
            for row in csvReader:
                channelA_sample.append(row[0])                                                     # For every row in in csvReader, the values are apended to green and red.         
                channelB_sample.append(row[1])
                a+=1
        
        print ("Loaded %s, which contains %s rows."%(filename,a))   
        
    channelA_arr_sample=np.asarray(channelA_sample,dtype=np.float32)                              # Converts these to numpy arrays for vector calcs.
    channelB_arr_sample=np.asarray(channelB_sample,dtype=np.float32)
    return channelA_arr_sample,channelB_arr_sample


def intensity_separate(input_file):
    small_events=input_file[np.logical_and(input_file>threshold_small, input_file<threshold_medium)] 
    medium_events=input_file[np.logical_and(input_file>threshold_medium, input_file<threshold_large)] 
    all_events=input_file[(input_file>threshold_small)]
    large_events=input_file[(input_file>threshold_large)]                 
    return all_events,small_events,medium_events,large_events

channelA_arr_sample,channelB_arr_sample=load_files_sample(number_of_files)

 
plt.plot(channelA_arr_sample)
# plt.xlim(0,800)
# plt.ylim(0,250)
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
