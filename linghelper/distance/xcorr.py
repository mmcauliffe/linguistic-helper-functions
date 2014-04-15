import math.log
import numpy as np
from scipy.signal import correlate,correlate2d,fftconvolve

def xcorr_distance(e1,e2):
    length_diff = e1.shape[0] - e2.shape[0]
    if length_diff > 0:
        longerEnv = e1
        shorterEnv = e2
    else:
        longerEnv = e2
        shorterEnv = e1
    num_bands = longerEnv.shape[1]
    matchSum = np.correlate(longerEnv[:,0],shorterEnv[:,0],mode='valid')
    corrs = [matchSum]
    for i in range(1,num_bands):
        temp = np.correlate(longerEnv[:,i],shorterEnv[:,i],mode='valid')
        corrs.append(temp)
        matchSum = [matchSum[j] + temp[j] for j in range(len(matchSum))]
    maxInd = np.argmax(matchSum)
    matchVal = matchSum[maxInd]/num_bands
    #if returnBandScores:
    #    return matchVal, [x[maxInd] for x in corrs]
    return -1*math.log(matchVal)

#def fft_correlate_envelopes(e1,e2):
    #length_diff = e1.shape[0] - e2.shape[0]
    #if length_diff > 0:
        #longerEnv = e1
        #shorterEnv = e2
    #else:
        #longerEnv = e2
        #shorterEnv = e1
    #num_bands = longerEnv.shape[1]
    #matchSum = fftconvolve(longerEnv[:,0],shorterEnv[:,0][::-1],mode='valid')
    #for i in range(1,num_bands):
        #temp = fftconvolve(longerEnv[:,i],shorterEnv[:,i][::-1],mode='valid')
        #matchSum = [matchSum[j] + temp[j] for j in range(len(matchSum))]
    #matchVal = max(matchSum)/num_bands
    #return matchVal