from numpy import log,array,zeros, floor,exp,sqrt,dot,arange, hanning,sin, pi,linspace,log10,round,maximum,minimum,sum,cos,spacing,diag
from numpy.fft import fft

from linghelper.phonetics.praat import PraatLoader
from linghelper.phonetics.praat.helper import to_array
from linghelper.phonetics.signal import preproc

from scipy.fftpack import dct
from scipy.io import wavfile



def filter_bank(nfft,nfilt,minFreq,maxFreq,sr):

    
    minMel = freqToMel(minFreq)
    maxMel = freqToMel(maxFreq)
    melPoints = linspace(minMel,maxMel,nfilt+2)
    binfreqs = melToFreq(melPoints)
    bins = round((nfft-1)*binfreqs/sr)

    fftfreqs = arange(int(nfft/2))/nfft * sr

    fbank = zeros([nfilt,int(nfft/2)])
    for i in range(nfilt):
        fs = binfreqs[i+arange(3)]
        fs = fs[1] + (fs - fs[1])
        loslope = (fftfreqs - fs[0])/(fs[1] - fs[0])
        highslope = (fs[2] - fftfreqs)/(fs[2] - fs[1])
        fbank[i,:] = maximum(zeros(loslope.shape),minimum(loslope,highslope))
    fbank = fbank / max(sum(fbank,axis=1))
    return fbank.transpose()

def freqToMel(freq):
    return 2595 * log10(1+freq/700.0)

def melToFreq(mel):
    return 700*(10**(mel/2595.0)-1)


def dct_spectrum(spec):
    ncep=spec.shape[0]
    dctm = zeros((ncep,ncep))
    for i in range(ncep):
        dctm[i,:] = cos(i * arange(1,2*ncep,2)/(2*ncep) * pi) * sqrt(2/ncep)
    dctm = dctm * 0.230258509299405
    cep =  dot(dctm , (10*log10(spec + spacing(1))))
    return cep

def to_melbank(filename, freq_lims,win_len,time_step,num_filters = 26):
    sr, proc = preproc(filename,alpha=0.97)
    
    minHz = freq_lims[0]
    maxHz = freq_lims[1]
    
    nperseg = int(win_len*sr)
    noverlap = int(time_step*sr)
    window = hanning(nperseg+2)[1:nperseg+1]
    
    filterbank = filter_bank(nperseg,num_filters,minHz,maxHz,sr)
    step = nperseg - noverlap
    indices = arange(0, proc.shape[-1]-nperseg+1, step)
    num_frames = len(indices)
    
    melbank = zeros((num_frames,num_filters))
    for k,ind in enumerate(indices):
        seg = proc[ind:ind+nperseg] * window
        complexSpectrum = fft(seg)
        powerSpectrum = abs(complexSpectrum[:int(nperseg/2)]) ** 2
        melbank[k,:] = dot(sqrt(powerSpectrum), filterbank)**2
    return melbank
    

def to_mfcc(filename, freq_lims,num_coeffs,win_len,time_step,num_filters = 26, use_power = False):
    #HTK style, interpreted from RastaMat
    sr, proc = preproc(filename,alpha=0.97)
    
    minHz = freq_lims[0]
    maxHz = freq_lims[1]
    
    L = 22
    n = arange(num_filters)
    lift = 1+ (L/2)*sin(pi*n/L)
    lift = diag(lift)
    
    nperseg = int(win_len*sr)
    noverlap = int(time_step*sr)
    window = hanning(nperseg+2)[1:nperseg+1]
    
    filterbank = filter_bank(nperseg,num_filters,minHz,maxHz,sr)
    step = nperseg - noverlap
    indices = arange(0, proc.shape[-1]-nperseg+1, step)
    num_frames = len(indices)
    
    mfccs = zeros((num_frames,num_coeffs))
    for k,ind in enumerate(indices):
        seg = proc[ind:ind+nperseg] * window
        complexSpectrum = fft(seg)
        powerSpectrum = abs(complexSpectrum[:int(nperseg/2)]) ** 2
        filteredSpectrum = dot(sqrt(powerSpectrum), filterbank)**2
        dctSpectrum = dct_spectrum(filteredSpectrum)
        dctSpectrum = dot(dctSpectrum , lift)
        if not use_power:
            dctSpectrum = dctSpectrum[1:]
        mfccs[k,:] = dctSpectrum[:num_coeffs]
    return mfccs


def to_mfcc_praat(filename, freq_lims, numCC,win_len,time_step):
    max_mel = freqToMel(freq_lims[1])
    scripts = {'mfcc.praat':"""
        form Variables
            sentence file
            positive numCC
            real windowLength
            real timeStep
            real maxMel
        endform

        Read from file... 'file$'

        To MFCC... numCC windowLength timeStep 100.0 100.0 maxMel

        To TableOfReal... 0
        
        output$ = ""
        
        numRows = Get number of rows
        
        for i from 1 to numRows
            for j from 1 to numCC
                val = Get value... i j
                val$ = fixed$(val,3)
                output$ = output$ + val$
                if j != numCC
                    output$ = output$ + tab$
                endif
            endfor
            if i != numRows
                output$ = output$ + newline$
            endif
        endfor

        echo 'output$'"""}
    p = PraatLoader(additional_scripts=scripts)
    output = p.run_script('mfcc.praat',filename,numCC,win_len,time_step,max_mel)
    return to_array(output)
    

