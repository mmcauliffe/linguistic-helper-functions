from numpy import log,fft,array,zeros

from linghelper.phonetics.praat import PraatLoader
from linghelper.phonetics.praat.helper import to_array

import numpy
from scipy.fftpack import dct
from scipy.io import wavfile



def melFilterBank(blockSize):
    numBands = int(numCoefficients)
    maxMel = int(freqToMel(maxHz))
    minMel = int(freqToMel(minHz))

    # Create a matrix for triangular filters, one row per filter
    filterMatrix = zeros((numBands, blockSize))

    melRange = array(range(numBands + 2))

    melCenterFilters = melRange * (maxMel - minMel) / (numBands + 1) + minMel

    # each array index represent the center of each triangular filter
    aux = numpy.log(1 + 1000.0 / 700.0) / 1000.0
    aux = (numpy.exp(melCenterFilters * aux) - 1) / 22050
    aux = 0.5 + 700 * blockSize * aux
    aux = numpy.floor(aux)  # Arredonda pra baixo
    centerIndex = numpy.array(aux, int)  # Get int values

    for i in xrange(numBands):
        start, centre, end = centerIndex[i:i + 3]
        k1 = numpy.float32(centre - start)
        k2 = numpy.float32(end - centre)
        up = (numpy.array(xrange(start, centre)) - start) / k1
        down = (end - numpy.array(xrange(centre, end))) / k2

        filterMatrix[i][start:centre] = up
        filterMatrix[i][centre:end] = down

    return filterMatrix.transpose()

def freqToMel(freq):
    return 1127.01048 * math.log(1 + freq / 700.0)

def melToFreq(mel):
    return 700 * (math.exp(freq / 1127.01048 - 1))

def to_mfcc_python(filename, freq_lims,numCC,windowLength,timeStep):
    sampleRate, signal = wavfile.read(filename)
    minHz = freq_lims[0]
    maxHz = freq_lims[1]
    win
    complexSpectrum = numpy.fft(signal)
    powerSpectrum = abs(complexSpectrum) ** 2
    filteredSpectrum = numpy.dot(powerSpectrum, melFilterBank())
    logSpectrum = numpy.log(filteredSpectrum)
    dctSpectrum = dct(logSpectrum, type=2)  # MFCC :)

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
    

