# Ali Ghavampour, Diedrichsenlab - 2023

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from modules import dataLoader
from modules import emgHandler
from modules.analysis import analysis
from efc1_emg_subj import efc1_emg_subj

scriptPath = os.getcwd()
analysisPath = scriptPath + '/analysis/'

def efc1_emg_create_subj_data(subjName):
    '''
        Description: Main code to create the data for each subject
    '''
    efc1_emg_subj(subjName)


def efc1_emg_analyze(dataName):
    '''
        Description: Main code to do analysis
    '''

    # loading data:
    D = pd.read_pickle(analysisPath + dataName)

    # making an analysis object:
    ANA = analysis(D)

    # pilot calssification of the emg data:
    ANA.pilot_classify_chord_emg(classify_interval_option=['hold'], fs=1000)



# creating data for each subject:
# subjName = ['subj99']
# for name in subjName:
#     efc1_emg_create_subj_data(name)


# analyzing data:
dataName = 'subj99.pkl'
efc1_emg_analyze(dataName=dataName)
