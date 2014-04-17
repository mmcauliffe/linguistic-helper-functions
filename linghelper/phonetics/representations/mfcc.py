from math import log10

from linghelper.phonetics.praat import PraatLoader
from linghelper.phonetics.praat.helper import to_array



def freq_to_mel(freq):
    return 2595 * log10(1+ (freq/700))

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
                val$ = fixed(val,3)
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
    output = p.run_script('mfcc.praat',*args)
    return to_array(output)
