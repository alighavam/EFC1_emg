import numpy as np
import pandas as pd
import os


def movload(fname):
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

    print(A[0][0:2])
    fid.close()
    return A


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
            movPath = scriptPath + '/data/' + subjName + '/efc1_' + \
                subjName[-2:] + '_' + '{:02d}.mov'.format(D.BN[i])
            mov = movload(movPath)
            # print(mov[0])
            oldBlock = D.BN[i]

    # print('Ali: ',movPath)

    ANA = D
    return ANA


ANA = efc1_emg_subj('subj99')
# print(ANA.loc[0])
