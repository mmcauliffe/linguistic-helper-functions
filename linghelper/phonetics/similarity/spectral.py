import sys
from linghelper.phonetics.praat import PraatLoader


def mfcc_distance(filename_one, filename_two, max_mel):
    scripts = {'mfcc_distance.praat':"""
        form Variables
            sentence firstfile
            sentence secondfile
            real maxMel
        endform

        Read from file... 'firstfile$'
        first = selected()

        Read from file... 'secondfile$'
        second = selected()

        select first
        To MFCC... 20 0.015 0.005 100.0 100.0 maxMel
        first_mfcc = selected()

        select second
        To MFCC... 20 0.015 0.005 100.0 100.0 maxMel
        second_mfcc = selected()


        select first_mfcc
        plus second_mfcc
        To DTW... 1.0 0.0 0.0 0.0 0.056 1 1 no restriction
        mfcc_dist = Get distance (weighted)

        echo 'mfcc_dist'"""}
    p = PraatLoader(additional_scripts=scripts)
    distance = p.run_script('mfcc_distance.praat',filename_one, filename_two, max_mel)
    return float(distance)

def spectral_distance(filename_one, filename_two,max_freq):
    scripts = {'spec_distance.praat':"""
        form Variables
            sentence firstfile
            sentence secondfile
            real maxFreq
        endform
        
        Read from file... 'firstfile$'
        first = selected()
        
        Read from file... 'secondfile$'
        second = selected()
        
        select first
        To Spectrogram... 0.005 maxFreq 0.002 20 Gaussian
        first_spec = selected()
        
        select second
        To Spectrogram... 0.005 maxFreq 0.002 20 Gaussian
        second_spec = selected()
        
        select first_spec
        plus second_spec
        To DTW... 1 1 no restriction
        spec_dist = Get distance (weighted)
        
        echo 'spec_dist'"""}
    p = PraatLoader(additional_scripts=scripts)
    distance = p.run_script('spec_distance.praat',filename_one, filename_two,max_freq)
    return float(distance)
