import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

def find_trigger_rise_edge(trig, fs, riseThresh=0.5, fallThresh=0.5, debug=0):    # detect rising and falling edges of the trigger signal
    
    # time vector for plotting the triggers:
    t = np.linspace(0,len(trig)/fs,len(trig)) 

    # normalizing the trigger signal to its abs maximum
    trig = trig/np.amax(np.absolute(trig))  

    # detecting rising edges:
    riseIdx, peak_heights = signal.find_peaks(trig, height=riseThresh)   

    # detecting falling edges:
    fallIdx, peak_heights = signal.find_peaks(-trig, height=fallThresh)
    

    if debug:   # debug mode to make sure of the trigger detection
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
        plt.plot(trig, label='trig')
        plt.plot(riseIdx, [trig[index] for index in riseIdx], 'ro', label='Rising Edges')
        plt.plot(fallIdx, [trig[index] for index in fallIdx], 'go', label='Falling Edges')
        # plt.xlim(4.3e+05,5e+05)
        plt.show()
        plt.legend()

        