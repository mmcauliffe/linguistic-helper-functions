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


def dct_spectrum(spec,ncep):
    nrow =spec.shape[0]
    dctm = zeros((ncep,nrow))
    for i in range(ncep):
        dctm[i,:] = cos(i * arange(1,2*nrow,2)/(2*nrow) * pi) * sqrt(2/nrow)
    dctm = dctm * 0.230258509299405
    cep =  dot(dctm , (10*log10(spec + spacing(1))))
    return cep

def to_mfcc(filename, freq_lims,numCC,win_len,time_step):
    #HTK style, interpreted from RastaMat
    numFilters = 20
    sr, proc = preproc(filename,alpha=0.97)
    
    minHz = freq_lims[0]
    maxHz = freq_lims[1]
    
    L = 22
    n = arange(numFilters)
    lift = 1+ (L/2)*sin(pi*n/L)
    lift = diag(lift)
    
    nperseg = int(win_len*sr)
    noverlap = int(time_step*sr)
    window = hanning(nperseg+2)[1:nperseg+1]
    
    filterbank = filter_bank(nperseg,numFilters,minHz,maxHz,sr)
    step = nperseg - noverlap
    indices = arange(0, proc.shape[-1]-nperseg+1, step)
    num_frames = len(indices)
    
    mfccs = zeros((num_frames,numCC))
    
    for k,ind in enumerate(indices):
        seg = proc[ind:ind+nperseg] * window
        complexSpectrum = fft(seg)
        powerSpectrum = abs(complexSpectrum[:int(nperseg/2)]) ** 2
        filteredSpectrum = dot(sqrt(powerSpectrum), filterbank)**2
        dctSpectrum = dct_spectrum(filteredSpectrum,numFilters)
        dctSpectrum = dot(dctSpectrum , lift)
        mfccs[k,:] = dctSpectrum[1:numCC+1]
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
    

