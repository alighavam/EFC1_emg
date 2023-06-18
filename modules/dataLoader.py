import numpy as np
import pandas as pd
from modules import emgHandler

def movload(fname):
    # loads .mov files given the path of the file. The .mov files have a specific custom hence the need for a custom function
    A = []
    fid = open(fname, 'rt')
    if fid == -1:
        raise Exception('Could not open ' + fname)

    trial = 0
    for line in fid:
        if line[0] == 'T':
            print('Trial: ', line.split()[1])
            a = int(line.split()[1])
            trial += 1
            if a != trial:
                print('Trials out of sequence')
                trial = a
            A.append([])
            A[trial-1] = np.empty((0,23))
        else:
            lineData = line.strip().split('\t')
            a = np.array([float(x) for x in lineData], ndmin=2)
            # print(a)
            A[trial-1] = np.vstack((A[trial-1],a))
            # A[trial-1].extend(a)

    fid.close()
    return A


def emgload(fname, riseThresh=0.5, fallThresh=0.5, debug=0): # handles loading emg files
    '''
        Description: Loads and handles the emg data from fname.csv file. 

        <inputs>
        fname: the .csv file name

        riseThresh, fallThresh, debug: refer to emgHandler.find_trigger_rise_edge function.

        <outputs>
        emg_selected: python list with len <number of trials>. Each list element is emg data for each tiral. It is a numpy array with the format of (N by ChannelNum). 
        N is the len of that trial. ChannelNum is the number of emg channels.

        fs: sampling frequency of the emg data.
    '''

    # loading emg file:
    column_names = [i for i in range(0, 7)] # hard coded number of columns in dataframe - ideally you should calculate maximum of number of columns for future use of the code
    data = pd.read_csv(fname, header=None, delimiter=',', names=column_names)   # loads .csv file into a dataframe
    fs = float(data[0][6].split()[0])   # getting the sampling rate of the data - hard coded to get fs. Also, assumed that all emg channels have the same fs.
    raw_emg = pd.DataFrame(data.iloc[7:], dtype=float)  # making a new dataframe containing only the raw emg data - hard coded row num
    raw_emg = raw_emg.reset_index(drop=True)
    
    # finding triggers:
    trig = raw_emg[0]   # trigger channel
    riseIdx, fallIdx = emgHandler.find_trigger_rise_edge(trig, fs, riseThresh, fallThresh, debug) # trigger detector function
    
    # slecting emg data of each trial based on triggers
    emg_selected = [] # empty list to contain emg data
    for i in range(len(riseIdx)):
        # starting index of trial i:
        idxStart = riseIdx[i]

        # ending index of trial i:
        idxEnd = fallIdx[i]     

        # selecting emg data. Channel 0 is trigger so it's not included:
        emg_tmp = raw_emg.iloc[idxStart:idxEnd,1:].to_numpy()  

        # append trial's emg data to emg_selected , the format of emg_tmp is (N by ChannelNum):
        emg_selected.append(emg_tmp)   
        # print("Trial {}:\n".format(i), len(emg_tmp[:,0])) # a sanity check
    
    # print(np.shape(emg_selected[99])) # sanity check
    return emg_selected, fs


