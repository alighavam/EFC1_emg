# Ali Ghavampour, Diedrichsenlab - 2023

import numpy as np
import pandas as pd
import os

from functions import dataLoader as dl

def efc1_emg_subj(subjName):
    scriptPath = os.getcwd()
    datFileName = scriptPath + '/data/' + subjName + \
        '/efc1_' + subjName[-2:] + '.dat'   # input .dat file
    outFileName = scriptPath + '/analysis/' + subjName + \
        '.csv'    # output file (saved to analyse folder)

    print(datFileName)
    print(outFileName)

    D = pd.read_table(datFileName)

    oldBlock = -1
    for i in range(len(D.BN)):
        if (oldBlock != D.BN[i]):
            # load mov file
            movPath = scriptPath + '/data/' + subjName + '/efc1_' + subjName[-2:] + '_' + '{:02d}.mov'.format(D.BN[i])
            mov = dl.movload(movPath)
            # print(mov[0])
            oldBlock = D.BN[i]

    # print('Ali: ',movPath)

    ANA = D
    return ANA


ANA = efc1_emg_subj('subj99')
# print(ANA.loc[0])
