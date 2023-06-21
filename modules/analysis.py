# Ali Ghavampour - 2023 - Diedrichsen Lab

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as pltv

class analysis:

    def __init__(self, dataframe):
        self.data = dataframe   # data given by the user


    def print_data(self):
        print(self.data)


    def pilot_classify_chord_emg(self, classify_interval_option, fs):
        '''
            Description: Classifies the chord from the emg data. This is a pilot function and should be modified for the final analysis.

            <inputs>
            interval_classify: This list contains characters that denote the interval that we would like to select the emg signals to decode the chords. Options are:
            'plan': The planning interval where no movement is hapenning -> Defenietly the decoding acc is small
            'RT': The selected interval is around the t_rt which is reaction time of the subject. t_rt is the time when the first finger moves out of the baseline zone.
            'hold': The hold time interval. This is the time that the subject is holding the chord.
            'exec': The first 200ms of the execution interval which starts at t_rt
            'all': All of the above intervals are selected.

            fs: sampling frequency of the emg data.
        '''
        # holder for the average emg signals:
        avg_emg_ext = []
        avg_emg_flx = []

        # classification for hold interval:
        if 'hold' in classify_interval_option:
            # holder for the average emg signals for each trial:
            emg_ext_hold_avg = np.zeros((len(self.data[(self.data['BN'] == 1) & (self.data['trialCorr'] == 1)]['emg']), 6))
            emg_flx_hold_avg = np.zeros((len(self.data[(self.data['BN'] == 2) & (self.data['trialCorr'] == 1)]['emg']), 6))
            
            # getting the emg data:
            emg_ext = self.data[(self.data['BN'] == 1) & (self.data['trialCorr'] == 1)]['emg']
            emg_flx = self.data[(self.data['BN'] == 2) & (self.data['trialCorr'] == 1)]['emg']

            # looping through each trial and averaging the emg signals:
            for i in range(len(emg_ext)):
                emg_ext_hold_avg[i, :] = np.mean(emg_ext.iloc[i][int(-1*0.6*fs):, :], axis=0)
                emg_flx_hold_avg[i, :] = np.mean(emg_flx.iloc[i][int(-1*0.6*fs):, :], axis=0)
            
            avg_emg_ext.append(emg_ext_hold_avg)
            avg_emg_flx.append(emg_flx_hold_avg)
        
        