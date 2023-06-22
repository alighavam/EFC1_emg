# Ali Ghavampour - 2023 - Diedrichsen Lab

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

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
        # This is just for this pilot analysis:
        # BN = 1 is the flexion block and BN = 2 is the extension block:
        ext_BN = 2
        flx_BN = 1

        # classification for hold interval:
        if 'hold' in classify_interval_option:
            # container for the average emg signals for each trial:
            emg_ext_hold_avg = np.zeros((len(self.data[(self.data['BN'] == ext_BN) & (self.data['trialCorr'] == 1)]['emg']), 6))
            emg_flx_hold_avg = np.zeros((len(self.data[(self.data['BN'] == flx_BN) & (self.data['trialCorr'] == 1)]['emg']), 6))
            
            # getting the emg data:
            emg_ext = self.data[(self.data['BN'] == ext_BN) & (self.data['trialCorr'] == 1)]['emg']
            emg_flx = self.data[(self.data['BN'] == flx_BN) & (self.data['trialCorr'] == 1)]['emg']

            # looping through each trial and averaging the emg signals:
            for i in range(len(emg_ext)):
                emg_ext_hold_avg[i, :] = np.mean(emg_ext.iloc[i][int(-1*0.6*fs):, :], axis=0)
            for i in range(len(emg_flx)):
                emg_flx_hold_avg[i, :] = np.mean(emg_flx.iloc[i][int(-1*0.6*fs):, :], axis=0)

            # getting chordIDs to make the dependant variable:
            chordID_ext = self.data[(self.data['BN'] == ext_BN) & (self.data['trialCorr'] == 1)]['chordID']
            chordID_flx = self.data[(self.data['BN'] == flx_BN) & (self.data['trialCorr'] == 1)]['chordID']

            # converting chordID to array:
            array_ext = [[int(x) for x in str(number)] for number in chordID_ext]
            array_flx = [[int(x) for x in str(number)] for number in chordID_flx]

            # converting the arrays to numpy arrays:
            y_ext = np.array(array_ext)
            y_flx = np.array(array_flx)

            # building the dependant variable:
            y_ext[y_ext == 9] = 0
            y_flx[y_flx == 2] = 1
            y_flx[y_flx == 9] = 0

            # visaulizing the average emg signals:
            plt.figure()
            for i in range(5):
                chord_data = emg_ext_hold_avg[y_ext[:,i] == 1,:]
                plt.errorbar(np.arange(6), np.mean(chord_data, axis=0), yerr=np.std(chord_data, axis=0), linestyle='None', marker='o', label='chord ' + str(i+1))

            plt.figure()
            for i in range(5):
                chord_data = emg_flx_hold_avg[y_flx[:,i] == 1,:]
                plt.errorbar(np.arange(6), np.mean(chord_data, axis=0), yerr=np.std(chord_data, axis=0), linestyle='None', marker='o', label='chord ' + str(i+1))
            # plt.legend()
            # plt.show()

            # linear regression - cross validated:
            # creating the folds:
            n_folds = 5
            train_size = 10
            train_ext_folds = []
            train_flx_folds = []
            test_ext_folds = []
            test_flx_folds = []
            # randomly selecting the trials for training and testing:
            for i in range(n_folds):
                # iterating through conditions:
                train_trials_ext = []
                train_trials_flx = []
                test_trials_ext = []
                test_trials_flx = []
                for j in range(5):
                    chord_trials_ext = np.where(y_ext[:,j] == 1)[0]
                    chord_trials_flx = np.where(y_flx[:,j] == 1)[0]

                    # randomly selecting the train trials for condition j:
                    train_idx_ext = np.random.choice(chord_trials_ext, train_size, replace=False)
                    train_idx_flx = np.random.choice(chord_trials_flx, train_size, replace=False)

                    # removing the selected indices from the chord_trials:
                    chord_trials_ext = np.setdiff1d(chord_trials_ext, train_idx_ext)
                    chord_trials_flx = np.setdiff1d(chord_trials_flx, train_idx_flx)

                    # adding the selected indices to the train_trials:
                    train_trials_ext.extend(train_idx_ext)
                    train_trials_flx.extend(train_idx_flx)

                    # adding the remaining indices to the test_trials:
                    test_trials_ext.extend(chord_trials_ext)
                    test_trials_flx.extend(chord_trials_flx)
                
                # adding the train folds to the train folds:
                train_ext_folds.append(train_trials_ext)
                train_flx_folds.append(train_trials_flx)

                # adding the test folds to the test folds:
                test_ext_folds.append(test_trials_ext)
                test_flx_folds.append(test_trials_flx)
            

            # looping through the folds and fitting the model:
            for i in range(n_folds):
                train_idx_ext = train_ext_folds[i]
                train_idx_flx = train_flx_folds[i]
                test_idx_ext = test_ext_folds[i]
                test_idx_flx = test_flx_folds[i]

                # getting the train and test data:
                x_train_ext = emg_ext_hold_avg[train_idx_ext, :]
                x_test_ext = emg_ext_hold_avg[test_idx_ext, :]
                y_train_ext = y_ext[train_idx_ext, :]
                y_test_ext = y_ext[test_idx_ext, :]

                x_train_flx = emg_flx_hold_avg[train_idx_flx, :]
                x_test_flx = emg_flx_hold_avg[test_idx_flx, :]
                y_train_flx = y_flx[train_idx_flx, :]
                y_test_flx = y_flx[test_idx_flx, :]

                # linear regression:
                beta_ext = np.linalg.inv(x_train_ext.T @ x_train_ext) @ x_train_ext.T @ y_train_ext
                beta_flx = np.linalg.inv(x_train_flx.T @ x_train_flx) @ x_train_flx.T @ y_train_flx

                # fitting to test data:
                yfit_ext = x_test_ext @ beta_ext
                yfit_flx = x_test_flx @ beta_flx

                # getting the max of the yfit:
                yfit_ext_max = np.array([yfit_ext[i,:]==max(yfit_ext[i,:]) for i in range(len(yfit_ext))])
                yfit_flx_max = np.array([yfit_flx[i,:]==max(yfit_flx[i,:]) for i in range(len(yfit_flx))])

                # calculating the accuracy:
                acc_ext = np.sum(yfit_ext_max * y_test_ext) / len(yfit_ext_max)
                acc_flx = np.sum(yfit_flx_max * y_test_flx) / len(yfit_flx_max)


                print('fold {}: acc ext = {} and acc flx = {}'.format(i, acc_ext, acc_flx))



            
        
        