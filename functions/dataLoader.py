import numpy as np

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