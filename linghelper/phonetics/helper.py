import math
#from scipy.fftpack import dct,idct
import numpy as np
from scipy.spatial.distance import euclidean

from praatinterface import PraatLoader

def get_intensity(filename, praat = None):
    if not praat:
        praat = PraatLoader()
    text = praat.run_script('intensity.praat',filename)
    return praat.read_praat_out(text)

def get_pitch(filename, praat = None):
    if not praat:
        praat = PraatLoader()
    text = praat.run_script('pitch.praat', filename)
    return praat.read_praat_out(text)

def to_ordered_list(time_dict,key=None):
    if key:
        return [time_dict[x][key] for x in sorted(time_dict.keys())]
    return [list(time_dict[x].values())[0] for x in sorted(time_dict.keys())]

def smooth(track, s):
    sortedtrack = sorted(track.keys())
    newtrack = {}
    for f in ['F1','F2','B1','B2']:
        for t in range(s,len(sortedtrack)-s):
            if f not in track[sortedtrack[t]]:
                continue
            smoothedF = track[sortedtrack[t]][f]
            for i in range(1,s+1):
                if f in track[sortedtrack[t+i]] and f in track[sortedtrack[t-i]]:
                    smoothedF += track[sortedtrack[t+i]][f] + track[sortedtrack[t-i]][f]
                else:
                    smoothedF = None
                    break
            if smoothedF:
                if sortedtrack[t] not in newtrack:
                    newtrack[sortedtrack[t]] = {}
                newtrack[sortedtrack[t]][f] = smoothedF / (2*s + 1)
    return newtrack

def DCT(time_series_data,num_coeff=None):
    """
    Calculate coefficients of a DCT-II analysis of time-normalized data.
    """
    coefficients = [0 for x in range(len(time_series_data))]
    N = float(len(time_series_data))
    for n,xn in enumerate(time_series_data):
        for m in range(len(coefficients)):
            coefficients[m] += xn * math.cos(((2*n+1)*m*math.pi)/(2*N))
    for m in range(len(coefficients)):
        if m == 0:
            k = 1/math.sqrt(2)
        else:
            k = 1
        coefficients[m] = coefficients[m]* (2*k)/N
    if num_coeff is not None:
        return coefficients[:num_coeff]
    return coefficients

def UnDCT(coefficients,N):
    """
    Create time series data from the coefficients of a DCT analysis.
    """
    time_series_data = []
    for n in range(N):
        at = 0
        for m in range(len(coefficients)):
            if m == 0:
                k = 1/math.sqrt(2)
            else:
                k = 1
            at += k * coefficients[m] * math.cos(((2*n +1)*m*math.pi)/(2*float(N)))
        time_series_data.append(at)
    return time_series_data

if __name__ == '__main__':
    data = [475.4,520.9,561.9,588.1,589.1]
    print(data)
    #data = [1,2,3,4,5,6,7,8]
    print(DCT(data))
    print(UnDCT(DCT(data)[:1],5))
    #print dct(data)
    #print idct(dct(data,norm="ortho"),norm="ortho")
    #print np.fft.rfft(data)
    print(euclidean(data,UnDCT(DCT(data)[:1],5)))
    print(euclidean(data,UnDCT(DCT(data)[:3],5)))
    print(euclidean(data,UnDCT(DCT(data)[:4],5)))
