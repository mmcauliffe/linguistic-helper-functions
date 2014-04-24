
from numpy import pi,exp,zeros,hanning,sum,arange,cos,sqrt
from scipy.fftpack import dct
from scipy.signal import hilbert
from linghelper.phonetics.signal import nextpow2,preproc,make_erb_cfs,fftfilt

def makeErbCfs(low_freq,high_freq,num_channels):
    return cfs

def to_mhec(path,numCC, num_bands, freq_lims, window_length,time_step):
    sr,proc = preproc(path)
    
    nperseg = int(window_length*sr)
    noverlap = int(time_step*sr)
    window = sqrt(hanning(window_length))
    
    cfs = make_erb_cfs(freq_lims,num_bands)

    filterOrder = 4 # filter order
    gL = 2**nextpow2(0.128*sr) # gammatone filter length at least 128 ms
    b = 1.019*24.7*(4.37*cfs/1000+1) # rate of decay or bandwidth
    phase = 0

    tpt=(2*pi)/sr
    gain=((1.019*b*tpt)**filterOrder)/6 # based on integral of impulse

    tmp_t = arange(gL)/sr

    step = nperseg - noverlap
    indices = arange(0, proc.shape[-1]-nperseg+1, step)
    num_frames = len(indices)
    S = zeros((num_frames,num_bands))
    
    mhecs = zeros((num_frames,numCC))

    # calculate impulse response
    for i in range(num_bands):
        gt = gain[i]*sr**3*tmp_t**(filterOrder-1)*exp(-2*pi*b[i]*tmp_t)*cos(2*pi*cfs[i]*tmp_t+phase)
        bm = fftfilt(gt,proc)
        env = abs(hilbert(bm))
        for k,ind in enumerate(indices):
            S[k,i] = sum(env[ind:ind+nperseg])
            
    for k in range(num_frames):
        mhecs[k,:] = dct(S[k,:],norm='ortho')[1:numCC+1]
    return mhecs
