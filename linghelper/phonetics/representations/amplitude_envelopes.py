from numpy import exp,log,abs,sum,sqrt,array

from scipy.signal import filtfilt,butter,hilbert,resample
from linghelper.phonetics.signal.helper import preproc,make_erb_cfs

def to_envelopes(path,num_bands,freq_lims,gammatone):
    sr, proc = preproc(path)
    sr_env = 60
    t = len(proc)/sr
    numsamp = t * sr_env * 2
    envelopes = []
    if gammatone:
        cfs = make_erb_cfs(freq_lims,num_bands)

        filterOrder = 4 # filter order
        gL = 2**nextpow2(0.128*sr) # gammatone filter length at least 128 ms
        b = 1.019*24.7*(4.37*cfs/1000+1) # rate of decay or bandwidth
        tc = np.zeros(cfs.shape)  # Initialise time lead
        phase = 0

        tpt=(2*pi)/sr
        gain=((1.019*b*tpt)**filterOrder)/6 # based on integral of impulse

        tmp_t = np.arange(gL)/sr

        # calculate impulse response
        for i in range(num_bands):
            gt = gain[i]*fs**3*tmp_t**(filterOrder-1)*exp(-2*pi*b[i]*tmp_t)*cos(2*pi*cfs[i]*tmp_t+phase)
            bm = fftfilt(gt,x)
            env = abs(hilbert(bm))
            env = resample(env,numsamp)
            denom = sqrt(sum(env**2))
            env = [x/denom for x in env]
            envelopes.append(env)
    else:
        bandLo = [ freq_lims[0]*exp(log(freq_lims[1]/freq_lims[0])/num_bands)**x for x in range(num_bands)]
        bandHi = [ freq_lims[0]*exp(log(freq_lims[1]/freq_lims[0])/num_bands)**(x+1) for x in range(num_bands)]

        for i in range(num_bands):
            b, a = butter(2,(bandLo[i]/(sr/2),bandHi[i]/(sr/2)), btype = 'bandpass')
            env = filtfilt(b,a,proc)
            env = abs(hilbert(env))
            env = resample(env,numsamp)
            denom = sqrt(sum(env**2))
            env = [x/denom for x in env]
            envelopes.append(env)
    return array(envelopes).T
    

