import numpy as np
import pandas as pd
import emgHandler

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


def emgload(fname): # handles loading emg files

    # loading emg file:
    column_names = [i for i in range(0, 7)]
    data = pd.read_csv(fname, header=None, delimiter=',', names=column_names)   # loads .csv file into a dataframe
    fs = float(data[0][6].split()[0])   # getting the sampling rate of the data
    raw_emg = pd.DataFrame(data.iloc[7:], dtype=float)  # making a new dataframe containing only the raw emg data
    raw_emg = raw_emg.reset_index(drop=True)
    
    # finding triggers:
    trig = raw_emg[0]   # trigger channel
    emgHandler.find_trigger_rise_edge(trig, fs, riseThresh=0.5, fallThresh=0.5, debug=1)
    


emgload('/Users/aghavampour/Desktop/Projects/ExtFlexChord/EFC1_emg/data/subj99/efc1_EMG_99_01.csv')