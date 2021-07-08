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

path_sample = r"/Users/Mathew/Documents/Edinburgh Code/Aggregate_Flow/Test_conc_data/asyn/500 nM/"           # This is the folder that contains the dye + sample
file_stem_sample="pftaa"   



number_of_files=3       # Number of files in the folder (could make this automatic in the future).

# Set the various thresholds here

threshold_small=40
threshold_medium=80
threshold_large=120



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





