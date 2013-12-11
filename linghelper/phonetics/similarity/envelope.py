
import math

from scipy.io import wavfile
from scipy.signal import filtfilt,butter,hilbert,correlate,correlate2d
import matplotlib.pyplot as plt

def snd2env(s, iFsOrig, fTotFreqRange, iNumBands, fEnvCutOff, fhEnvMethod, iFsNew):
    bandLo = [ fTotFreqRange[0]*math.pow(math.exp(math.log(fTotFreqRange[1]/fTotFreqRange[0])/iNumBands),x) for x in range(iNumBands)]
    bandHi = [ fTotFreqRange[0]*math.pow(math.exp(math.log(fTotFreqRange[1]/fTotFreqRange[0])/iNumBands),x+1) for x in range(iNumBands)]
    CFs = [bandLo[x] * math.sqrt(bandHi[x]/bandLo[x]) for x in range(iNumBands)]
    print(bandLo)
    print(bandHi)
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
        maxLag = length_diff
    else:
        longerEnv = e2
        shorterEnv = e1
        maxLag = -length_diff
    print(maxLag)
    matchSum = correlate(longerEnv[0],shorterEnv[0],mode='valid')
    print(len(matchSum))
    for i in range(1,len(longerEnv)):
        temp = correlate(longerEnv[i],shorterEnv[i],mode='valid')
        matchSum = [matchSum[j] + temp[j] for j in range(len(matchSum))]
    matchVal = max(matchSum)/len(longerEnv)

    print(matchVal)
    #matchSum = [0 for x in ]

if __name__ == '__main__':
    path_one = '/home/michael/Documents/Grad/PhD/MollyLab/NZDiph/Scripting/AUModelTokens/spare.wav'
    path_two = '/home/michael/Documents/Grad/PhD/MollyLab/NZDiph/Scripting/AUModelTokens/fare.wav'
    sr,sigone = wavfile.read(path_one)
    print(sr)
    env_one = snd2env(sigone,sr,(80,7800),4,60,'','')
    plt.plot(env_one,range(len(env_one)))
    plt.show()
    sr,sigtwo = wavfile.read(path_two)
    env_two = snd2env(sigtwo,sr,(80,7800),4,60,'','')
    envelope_match(env_one,env_two)
