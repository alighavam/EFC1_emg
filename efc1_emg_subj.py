# Ali Ghavampour, Diedrichsenlab - 2023

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from functions import dataLoader

def efc1_emg_subj(subjName):
    scriptPath = os.getcwd()
    datFileName = scriptPath + '/data/' + subjName + \
        '/efc1_' + subjName[-2:] + '.dat'   # input .dat file
    outFileName = scriptPath + '/analysis/' + subjName + \
        '.csv'    # output file (saved to analyse folder)

    print(datFileName)
    print(outFileName)

    D = pd.read_table(datFileName)
    D = D.loc[:, ~D.columns.str.contains('^Unnamed')]

    # loading mov files and appending each block to movList:
    oldBlock = -1
    movList = []
    for i in range(len(D.BN)):
        if (oldBlock != D.BN[i]):
            # load mov file
            movPath = scriptPath + '/data/' + subjName + '/efc1_' + subjName[-2:] + '_' + '{:02d}.mov'.format(D.BN[i])
            mov = dataLoader.movload(movPath)
            movList.extend(mov)
            # print(mov[0])
            oldBlock = D.BN[i]
            print(len(movList))

    # adding the mov data to the dataframe
    D['mov'] = movList

    # loading emg data:
    emgList = [] # list to contain all emg trials

    # iterate through emg files and load:
    uniqueBN = np.unique(D.BN)
    for i in range(len(uniqueBN)):
        # getting the name of the file:
        fname = scriptPath + '/data/' + subjName + '/efc1_EMG_' + subjName[-2:] + '_' + '{:02d}.csv'.format(uniqueBN[i])

        # loading emg and separating trials:
        emg_selected, fs = dataLoader.emgload(fname, riseThresh=0.5, fallThresh=0.5, debug=0)

        # bandpass filtering the signals:
        

        # adding emg data of trials to emgList:
        emgList.extend(emg_selected)

    # adding emg data to the dataframe:
    D['emg'] = emgList

    plt.plot(emg_selected[0][:,1])
    plt.show()

    return D


ANA = efc1_emg_subj('subj99')
print(ANA)
