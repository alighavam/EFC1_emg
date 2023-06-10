import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

def find_trigger_rise_edge(trig, fs, riseThresh=0.5, fallThresh=0.5, debug=0):    # detect rising and falling edges of the trigger signal
    '''
        Description: Detects triggers from the trigger channel of the data.

        <inputs>
        trig: emg channel that records triggers. For my case it should always be the first channel.

        fs: sampling rate of the data. Should be accessible from the .csv file of the emg.

        riseThresh: The threshold to detect the rising edge of the trigger. Note that trigger data is normalized to its maximum absolute value in this function.
        So threhshold values are from 0 to 1. The rise edge in my data denotes the start of a trial.

        fallThresh: Same as riseThresh but for falling edges. The fall edge denotes the end of a trial in my data.

        debug: debug mode. Plots the detected triggers for eye insepction. Also, prints some sanity checks in the console. Make sure to run the function with the debug mode 1 
        the first time that you are detecting triggers in a trigger channel. Basically run in debug mode every block of the emg data.

        <outputs>
        riseIdx: Contains the indices in the emg data that rising index was detected. In other words the indices that trial was started. Note that this is an index not 
        a time.

        fallIdx: Same as riseIdx but for falling edge. End index of each trial.
    ''' 

    # time vector for plotting the triggers:
    t = np.linspace(0,len(trig)/fs,len(trig)) 

    # normalizing the trigger signal to its abs maximum
    trig = trig/np.amax(np.absolute(trig))  

    # detecting rising edges:
    riseIdx, peak_heights = signal.find_peaks(trig, height=riseThresh)   

    # detecting falling edges:
    fallIdx, peak_heights = signal.find_peaks(-trig, height=fallThresh)

    # debug mode to make sure of the trigger detection:
    if debug:   
        # number of detected triggers:
        print("\n\n======== Trigger Detection Results: ======== \n")
        print("Num Rise Trigger = {:d}".format(len(riseIdx)))
        print("Num Fall Triggers = {:d}".format(len(fallIdx)))
        print("Two numbers should be equal to the number of trials.\n")

        # falling edge triggers should be always after rising edge:
        if len(fallIdx) == len(riseIdx):
            diffRiseFall = fallIdx - riseIdx
            numNegative = sum(diffRiseFall <= 0)
            print("\nNumber of non-positive fall-rise edges = {:d}".format(numNegative))
            print("This value should be 0.\n")

        # plotting trigger signal along with the detected triggers:
        plt.figure()
        plt.plot(trig, label='trig')
        plt.plot(riseIdx, [trig[index] for index in riseIdx], 'ro', label='Rising Edges')
        plt.plot(fallIdx, [trig[index] for index in fallIdx], 'go', label='Falling Edges')
        # plt.xlim(4.3e+05,5e+05)
        plt.show()

    return riseIdx, fallIdx
    

def bandpass_emg(emg, fs, low=20, high=500, order=2):
    
    # designing the filter:
    sos = signal.butter(order, [low, high], btype='bandpass', fs=fs, output='sos')

    # iterating through signals and filtering:
    for i in range(emg):
        