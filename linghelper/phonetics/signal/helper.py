from numpy import abs, log2, ceil, mean,sqrt,log10,linspace,array
from scipy.io import wavfile
from scipy.signal import lfilter,resample

def nextpow2(x):
    """Return the first integer N such that 2**N >= abs(x)"""
    
    return ceil(log2(abs(x)))


def preproc(path,sr=16000):
    oldsr,sig = wavfile.read(path)
    if sr != oldsr:
        t = len(sig)/oldsr
        numsamp = t * sr
        proc = resample(sig,numsamp)
    else:
        proc = sig
    #proc = lfilter(1, [1, -0.95],proc)
    denom = sqrt(mean([x**2 for x in proc]))
    proc = [ x/denom *0.03 for x in proc]
    return sr,array(proc)

def erb_rate_to_hz(x):
    y=(10**(x/21.4)-1)/4.37e-3
    return y
    
def hz_to_erb_rate(x):
    y=(21.4*log10(4.37e-3*x+1))
    return y

def make_erb_cfs(freq_lims,num_channels):
    cfs = erb_rate_to_hz(linspace(hz_to_erb_rate(freq_lims[0]),hz_to_erb_rate(freq_lims[1]),num_channels))
    return cfs
