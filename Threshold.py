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

path_control = r"/Users/Mathew/Documents/Edinburgh Code/Aggregate_Flow/Test_conc_data/PFTAA calibration/0 nM/"           # This is the folder that contains the dye only
file_stem_control="pftaa"                     # This is the filename before the underscore. 

path_sample = r"/Users/Mathew/Documents/Edinburgh Code/Aggregate_Flow/Test_conc_data/PFTAA calibration/500 nM/"           # This is the folder that contains the dye + sample
file_stem_sample="pftaa"   



number_of_files=1       # Number of files in the folder (could make this automatic in the future).




def load_files_control(number_of_files):
    
    channelA_control=[]             # Where channel A data will be stored
    channelB_control=[]             # Where channel B data will be stored
    for i in range(0,number_of_files):
        
        if(i<1):
            filename=path_control+file_stem_control
        elif(i<10):
            filename=path_control+file_stem_control+"_0"+str(i+1)
        else:
            filename=path_control+file_stem_control+"_"+str(i+1)
        a=0                                                                             # Row counter
        with open(filename) as csvDataFile:                                                # Opens the file as a CSV
            csvReader = csv.reader(csvDataFile,delimiter='\t')                           # Assigns the loaded CSV file to csvReader. 
            for row in csvReader:
                channelA_control.append(row[0])                                                     # For every row in in csvReader, the values are apended to green and red.         
                channelB_control.append(row[1])
                a+=1
        
        print("Loaded %s, which contains %s rows."%(filename,a))   
        
    channelA_arr_control=np.asarray(channelA_control,dtype=np.float32)                              # Converts these to numpy arrays for vector calcs.
    channelB_arr_control=np.asarray(channelB_control,dtype=np.float32)
    return channelA_arr_control,channelB_arr_control

channelA_arr_control,channelB_arr_control=load_files_control(number_of_files)


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

channelA_arr_sample,channelB_arr_sample=load_files_sample(number_of_files)



plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = "12"
plt.figure(figsize=(8, 6))
plt.plot(channelA_arr_sample,color='#ff0000',alpha=0.5,label="Sample Events")
plt.plot(channelA_arr_control,color='#cccccc',alpha=0.5,label="Control Events")         
plt.xlim(1740000,1760000)
plt.ylim(0,200)
plt.legend(loc='upper right')         
plt.xlabel('Bin number')
plt.ylabel('Photons/bin')
plt.show()


def threshtest():
    sample = np.zeros(shape=(5000))
    control = np.zeros(shape=(5000))
    fraction_events=np.zeros(shape=(5000))
    for A in range(0,200):
    
        # go through sample first
        channelA_real_events=channelA_arr_sample[(channelA_arr_sample>A)]                       # Total A events
        
        
         # go through control 
        channelA_control_events=channelA_arr_control[(channelA_arr_control>A)]                       # Total A events
        
        
        
        var_real_events=float(len(channelA_real_events))
        var_control_events=float(len(channelA_control_events))
        
        if(var_control_events>0):
            var_frac=float(var_real_events/var_control_events)
        else:
             var_frac=1
        
        sample[A]=var_real_events
        control[A]=var_control_events
        fraction_events[A]=var_frac
        

    maximum_frac=np.amax(fraction_events)
    result=np.where(fraction_events == np.amax(fraction_events))
    var_real_events_thresh=sample[result]
    var_control_events_thresh=control[result]
    
    
    
    Threshold=result
    
    print('The maximum ratio of real events is %.3f, with a threshold of %s in channel A. This gave %.3f real events, %.3f control events.'%(maximum_frac,str(Threshold),var_real_events_thresh,var_control_events_thresh))
    
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["font.size"] = "12"
    plt.figure(figsize=(8, 6))
    plt.plot(control,color='#cccccc',alpha=0.5,label="Control Events")
    plt.plot(sample,color='#ff0000',alpha=0.5,label="Sample Events")      
    plt.xlim(40,200)
    plt.ylim(0,50)
    plt.legend(loc='upper right')         
    plt.xlabel('Threshold (photons/bin)')
    plt.ylabel('Number of Events')
    plt.show()
    
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["font.size"] = "12"
    plt.figure(figsize=(8, 6))
    plt.plot(fraction_events,color='#0000ff',alpha=0.5,label="Sample/Control")  
    plt.xlim(40,200)
    plt.legend(loc='upper right')         
    plt.xlabel('Threshold (photons/bin)')
    plt.ylabel('Number of events')
    plt.show()
         
threshtest()


sbr_control=channelA_arr_control/channelA_arr_control.mean()
sbr_sample=channelA_arr_sample/channelA_arr_sample.mean()


