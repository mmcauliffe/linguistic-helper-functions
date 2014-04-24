from numpy import log,fft,array,zeros, floor,exp,sqrt,dot,arange

from linghelper.phonetics.praat import PraatLoader
from linghelper.phonetics.praat.helper import to_array

import numpy
from scipy.fftpack import dct
from scipy.io import wavfile



def melFilterBank(blockSize,numBands,minMel,maxMel):

    # Create a matrix for triangular filters, one row per filter
    filterMatrix = zeros((numBands, blockSize))

    melRange = arange(numBands + 2)

    melCenterFilters = melRange * (maxMel - minMel) / (numBands + 1) + minMel

    # each array index represent the center of each triangular filter
    aux = log(1 + 1000.0 / 700.0) / 1000.0
    aux = (exp(melCenterFilters * aux) - 1) / 22050
    aux = 0.5 + 700 * blockSize * aux
    aux = floor(aux)  
    centerIndex = array(aux, int)

    for i in range(numBands):
        start, centre, end = centerIndex[i:i + 3]
        k1 = float64(centre - start)
        k2 = float64(end - centre)
        up = (arange(start, centre)) - start) / k1
        down = (end - arange(centre, end))) / k2

        filterMatrix[i][start:centre] = up
        filterMatrix[i][centre:end] = down

    return filterMatrix.transpose()

def freqToMel(freq):
    return 1127.01048 * math.log(1 + freq / 700.0)

def melToFreq(mel):
    return 700 * (math.exp(freq / 1127.01048 - 1))

def to_mfcc_python(filename, freq_lims,numCC,windowLength,timeStep):
    sr, signal = wavfile.read(filename)
    
    minHz = freq_lims[0]
    maxHz = freq_lims[1]
    maxMel = int(freqToMel(maxHz))
    minMel = int(freqToMel(minHz))
    
    nperseg = int(window_length*sr)
    noverlap = int(time_step*sr)
    window = sqrt(hanning(nperseg))
    
    filterbank = melFilterBank(nperseg,numCC+1,minMel,maxMel)
    
    step = nperseg - noverlap
    indices = arange(0, proc.shape[-1]-nperseg+1, step)
    num_frames = len(indices)
    
    mfccs = zeros(num_frames,numCC)
    
    for k,ind in enumerate(indices):
        seg = signal[ind:ind+nperseg] * window
        complexSpectrum = fft(seg)
        powerSpectrum = abs(complexSpectrum) ** 2
        filteredSpectrum = dot(powerSpectrum, filterbank)
        logSpectrum = log(filteredSpectrum)
        dctSpectrum = dct(logSpectrum, norm='ortho')
        mfccs[k,:] = dctSpectrum[1:]
    return mfccs

def to_mfcc(filename,numCC,windowLength,timeStep,max_mel):
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
    output = p.run_script('mfcc.praat',filename,numCC,windowLength,timeStep,max_mel)
    return to_array(output)
    

