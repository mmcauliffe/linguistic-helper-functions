
import math

from scipy.io import wavfile
from scipy.signal import filtfilt,butter,hilbert,correlate,correlate2d,lfilter
import matplotlib.pyplot as plt

import numpy as np

def snd2env(s, iFsOrig, fTotFreqRange, iNumBands, fEnvCutOff):
    bandLo = [ fTotFreqRange[0]*math.pow(math.exp(math.log(fTotFreqRange[1]/fTotFreqRange[0])/iNumBands),x) for x in range(iNumBands)]
    bandHi = [ fTotFreqRange[0]*math.pow(math.exp(math.log(fTotFreqRange[1]/fTotFreqRange[0])/iNumBands),x+1) for x in range(iNumBands)]

    sB = []
    for i in range(iNumBands):
        b, a = butter(2,(bandLo[i]/(iFsOrig/2),bandHi[i]/(iFsOrig/2)), btype = 'bandpass')
        sB.append(filtfilt(b,a,s))

    e = []
    b, a = butter(4, fEnvCutOff/(iFsOrig/2),btype = 'low')
    for i in range(iNumBands):
        env = [abs(x) for x in hilbert(sB[i])]
        env = filtfilt(b,a, env)
        denom = math.sqrt(sum([math.pow(y,2) for y in env]))
        env = [x/denom for x in env]
        e.append(env)

    return e

def envelope_match(e1,e2):
    length_diff = len(e1[0]) - len(e2[0])
    if length_diff > 0:
        longerEnv = e1
        shorterEnv = e2
    else:
        longerEnv = e2
        shorterEnv = e1
    matchSum = np.correlate(longerEnv[0],shorterEnv[0],mode='valid')
    for i in range(1,len(longerEnv)):
        temp = np.correlate(longerEnv[i],shorterEnv[i],mode='valid')
        matchSum = [matchSum[j] + temp[j] for j in range(len(matchSum))]
    matchVal = max(matchSum)/len(longerEnv)

    return matchVal

def preproc(sig):
    proc = sig
    #proc = lfilter(1, [1, -0.95],sig)
    denom = math.sqrt(np.mean([math.pow(x,2) for x in proc]))
    proc = [ x/denom *0.03 for x in proc]
    return proc

def calc_envelope(path,num_bands=4):
    sr,sig = wavfile.read(path)
    proc = preproc(sig)
    env = snd2env(proc,sr,(80,7800),num_bands,60)
    return env

def envelope_similarity(path_one,path_two,num_bands=4):
    env_one = calc_envelope(path_one,num_bands = num_bands)
    env_two = calc_envelope(path_two,num_bands = num_bands)
    matchVal = envelope_match(env_one, env_two)
    return matchVal


if __name__ == '__main__':
    import time
    start_time = time.time()
    path_one = '/home/michael/Documents/Grad/PhD/MollyLab/NZDiph/Scripting/AUModelTokens/spare.wav'
    path_two = '/home/michael/Documents/Grad/PhD/MollyLab/NZDiph/Scripting/AUModelTokens/fare.wav'
    sr,sigone = wavfile.read(path_one)
    print(sr)
    env_one = snd2env(sigone,sr,(80,7800),8,60)
    plt.plot(env_one,range(len(env_one)))
    plt.show()
    sr,sigtwo = wavfile.read(path_two)
    env_two = snd2env(sigtwo,sr,(80,7800),8,60)
    print('envelopes generated')
    match_time = time.time()
    print(envelope_match(env_one,env_two))
    print(time.time() - match_time)
