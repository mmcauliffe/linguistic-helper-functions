import math

import numpy as np

from scipy.io import wavfile
from scipy.signal import filtfilt,butter,hilbert,lfilter,resample

def preproc(sig,sr,newSr=16000):
    t = len(sig)/sr
    numsamp = t * newSr
    proc = resample(sig,numsamp)
    #proc = lfilter(1, [1, -0.95],sig)
    denom = math.sqrt(np.mean([math.pow(x,2) for x in proc]))
    proc = [ x/denom *0.03 for x in proc]
    return newSr,proc

def to_envelopes(path,num_bands,freq_lims,erb):
    sr,sig = wavfile.read(path)
    sr, proc = preproc(sig,sr)
    if erb:
        env = snd2ERBenv(proc,sr,freq_lims,num_bands,60)
    else:
        env = snd2env(proc,sr,freq_lims,num_bands,60)
    return np.array(env).T
    
def snd2env(s, sr_orig, freq_range, num_bands, sr_env):
    bandLo = [ freq_range[0]*math.pow(math.exp(math.log(freq_range[1]/freq_range[0])/num_bands),x) for x in range(num_bands)]
    bandHi = [ freq_range[0]*math.pow(math.exp(math.log(freq_range[1]/freq_range[0])/num_bands),x+1) for x in range(num_bands)]

    e = []
    t = len(s)/sr_orig
    numsamp = t * sr_env * 2
    for i in range(num_bands):
        b, a = butter(2,(bandLo[i]/(sr_orig/2),bandHi[i]/(sr_orig/2)), btype = 'bandpass')
        env = filtfilt(b,a,s)
        env = np.abs(hilbert(env))
        env = resample(env,numsamp)
        denom = math.sqrt(sum(np.power(env,2)))
        env = [x/denom for x in env]
        e.append(env)

    return e

def snd2ERBenv(s,SR,freq_range,num_bands, sr_env):
    cfs = erbspace(freq_range[0],freq_range[1],num_bands)
    e = []
    t = len(s)/SR
    numsamp = t * sr_env * 2
    #bEnv, aEnv = butter(4, EnvSr/(SR/2),btype = 'low')
    for i in range(num_bands):
        bw = ERB(cfs[i])
        bandLo = cfs[i] - (bw/2)
        bandHi = cfs[i] + (bw/2)
        b, a = butter(2,(bandLo/(SR/2),bandHi/(SR/2)), btype = 'bandpass')
        env = filtfilt(b,a,s)
        env = np.abs(hilbert(env))
        env = resample(env,numsamp)
        denom = math.sqrt(sum(np.power(env,2)))
        env = [x/denom for x in env]
        e.append(env)
    return e
    

def ERB(cf):
    erb = 24.7 * (4.37*(cf/1000) + 1)
    return erb