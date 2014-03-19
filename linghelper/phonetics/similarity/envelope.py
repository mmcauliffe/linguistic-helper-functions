
import math

from scipy.io import wavfile
from scipy.signal import filtfilt,butter,hilbert,correlate,correlate2d,lfilter,fftconvolve,resample

import numpy as np

def snd2env(s, iFsOrig, fTotFreqRange, iNumBands, fEnvCutOff):
    bandLo = [ fTotFreqRange[0]*math.pow(math.exp(math.log(fTotFreqRange[1]/fTotFreqRange[0])/iNumBands),x) for x in range(iNumBands)]
    bandHi = [ fTotFreqRange[0]*math.pow(math.exp(math.log(fTotFreqRange[1]/fTotFreqRange[0])/iNumBands),x+1) for x in range(iNumBands)]

    e = []
    t = len(s)/iFsOrig
    numsamp = t * fEnvCutOff * 2
    for i in range(iNumBands):
        b, a = butter(2,(bandLo[i]/(iFsOrig/2),bandHi[i]/(iFsOrig/2)), btype = 'bandpass')
        sB = filtfilt(b,a,s)
        env = np.abs(hilbert(sB))
        env = resample(env,numsamp)
        denom = math.sqrt(sum(np.power(env,2)))
        env = [x/denom for x in env]
        e.append(env)

    return e

def snd2ERBenv(s,SR,bounds=(80,7800),num_bands=128):
    EnvSr = 60
    cfs = erbspace(bounds[0],bounds[1],num_bands)
    e = []
    t = len(s)/SR
    numsamp = t * EnvSr * 2
    #bEnv, aEnv = butter(4, EnvSr/(SR/2),btype = 'low')
    for i in range(num_bands):
        bw = ERB(cfs[i])
        bandLo = cfs[i] - (bw/2)
        bandHi = cfs[i] + (bw/2)
        b, a = butter(2,(bandLo/(SR/2),bandHi/(SR/2)), btype = 'bandpass')
        env = filtfilt(b,a,s)
        env = np.abs(hilbert(env))
        #env = filtfilt(bEnv,aEnv,env)
        env = resample(env,numsamp)
        denom = math.sqrt(sum(np.power(env,2)))
        env = [x/denom for x in env]
        e.append(env)
    return e


def correlate_envelopes(e1,e2,returnBandScores = False):
    length_diff = len(e1[0]) - len(e2[0])
    if length_diff > 0:
        longerEnv = e1
        shorterEnv = e2
    else:
        longerEnv = e2
        shorterEnv = e1
    matchSum = np.correlate(longerEnv[0],shorterEnv[0],mode='valid')
    corrs = [matchSum]
    for i in range(1,len(longerEnv)):
        temp = np.correlate(longerEnv[i],shorterEnv[i],mode='valid')
        corrs.append(temp)
        matchSum = [matchSum[j] + temp[j] for j in range(len(matchSum))]
    maxInd = np.argmax(matchSum)
    matchVal = matchSum[maxInd]/len(longerEnv)
    if returnBandScores:
        return matchVal, [x[maxInd] for x in corrs]
    return matchVal

def preproc(sig,sr,newSr=16000):
    t = len(sig)/sr
    numsamp = t * newSr
    proc = resample(sig,numsamp)
    #proc = lfilter(1, [1, -0.95],sig)
    denom = math.sqrt(np.mean([math.pow(x,2) for x in proc]))
    proc = [ x/denom *0.03 for x in proc]
    return newSr,proc

def calc_envelope(path,num_bands,freq_lims,erb):
    sr,sig = wavfile.read(path)
    sr, proc = preproc(sig,sr)
    if erb:
        env = snd2ERBenv(proc,sr,num_bands=num_bands)
    else:
        env = snd2env(proc,sr,(80,7800),num_bands,60)
    return env

def envelope_similarity(path_one,path_two,num_bands=4,erb=False):
    env_one = calc_envelope(path_one,num_bands = num_bands,erb=erb)
    env_two = calc_envelope(path_two,num_bands = num_bands,erb=erb)
    matchVal = envelope_match(env_one, env_two)
    return matchVal

def ERB(cf):
    erb = 24.7 * (4.37*(cf/1000) + 1)
    return erb

def figure_bands(lowfreq,highfreq,nbands):
    pass

def fft_envelope_match(e1,e2):
    length_diff = len(e1[0]) - len(e2[0])
    if length_diff > 0:
        longerEnv = e1
        shorterEnv = e2
    else:
        longerEnv = e2
        shorterEnv = e1
    matchSum = fftconvolve(longerEnv[0],shorterEnv[0][::-1],mode='valid')
    for i in range(1,len(longerEnv)):
        temp = fftconvolve(longerEnv[i],shorterEnv[i][::-1],mode='valid')
        matchSum = [matchSum[j] + temp[j] for j in range(len(matchSum))]
    matchVal = max(matchSum)/len(longerEnv)
    return matchVal

def test_envelope_matching():
    import time
    start_time = time.time()
    path_one = '/home/michael/Documents/Grad/PhD/MollyLab/NZDiph/Scripting/AUModelTokens/spare.wav'
    path_two = '/home/michael/Documents/Grad/PhD/MollyLab/NZDiph/Scripting/AUModelTokens/spear.wav'
    sr,sigone = wavfile.read(path_one)
    sr,sigtwo = wavfile.read(path_two)
    print('envelopes generating')
    gen_time = time.time()
    env_one = snd2env(sigone,sr,(80,7800),8,60)
    env_two = snd2env(sigtwo,sr,(80,7800),8,60)
    print('time: ',time.time() - gen_time)
    print('current matching')
    match_time = time.time()
    print('value: ',envelope_match(env_one,env_two))
    print('time: ',time.time() - match_time)
    print('old matching')
    new_match_time = time.time()
    print('value: ',fft_envelope_match(env_one,env_two))
    print('time: ',time.time() - new_match_time)

def test_ERBenv_matching():
    import time
    start_time = time.time()
    path_one = '/home/michael/Documents/Grad/PhD/MollyLab/NZDiph/Scripting/AUModelTokens/spare.wav'
    path_two = '/home/michael/Documents/Grad/PhD/MollyLab/NZDiph/Scripting/AUModelTokens/spear.wav'
    sr,sigone = wavfile.read(path_one)
    sr,sigtwo = wavfile.read(path_two)
    print('envelopes generating')
    gen_time = time.time()
    env_two = snd2ERBenv(sigtwo,sr)
    env_one = snd2ERBenv(sigone,sr)
    print('time: ',time.time() - gen_time)
    print('current matching')
    match_time = time.time()
    print('value: ',envelope_match(env_one,env_two))
    print('time: ',time.time() - match_time)
    print('old matching')
    new_match_time = time.time()
    print('value: ',fft_envelope_match(env_one,env_two))
    print('time: ',time.time() - new_match_time)

def erbspace(low, high, N, earQ=9.26449, minBW=24.7, order=1):
    '''
    Returns the centre frequencies on an ERB scale.

    ``low``, ``high``
        Lower and upper frequencies
    ``N``
        Number of channels
    ``earQ=9.26449``, ``minBW=24.7``, ``order=1``
        Default Glasberg and Moore parameters.
    '''
    low = float(low)
    high = float(high)
    cf = -(earQ * minBW) + np.exp((np.arange(N)) * (-np.log(high + earQ * minBW) + \
            np.log(low + earQ * minBW)) / (N-1)) * (high + earQ * minBW)
    cf = cf[::-1]
    return cf

def test_lazy():
    import audiolazy as lz

def brian():
    cfs = erbspace(80,8000,128)

    print(cfs)

if __name__ == '__main__':
    test_ERBenv_matching()
    test_envelope_matching()
