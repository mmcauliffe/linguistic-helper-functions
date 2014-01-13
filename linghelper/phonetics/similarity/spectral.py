import sys
sys.path.append('/home/michael/dev/Linguistics/python-praat-scripts')
from praatinterface import PraatLoader

from scipy.spatial.distance import euclidean


def mfcc_distance(filename_one, filename_two):
    scripts = {'mfcc_distance.praat':"""form Variables
                                            sentence firstfile
                                            sentence secondfile
                                        endform

                                        Read from file... 'firstfile$'
                                        first = selected()

                                        Read from file... 'secondfile$'
                                        second = selected()

                                        select first
                                        To MFCC... 20 0.015 0.005 100.0 100.0 0.0
                                        first_mfcc = selected()

                                        select second
                                        To MFCC... 20 0.015 0.005 100.0 100.0 0.0
                                        second_mfcc = selected()


                                        select first_mfcc
                                        plus second_mfcc
                                        To DTW... 1.0 0.0 0.0 0.0 0.056 1 1 no restriction
                                        mfcc_dist = Get distance (weighted)

                                        echo 'mfcc_dist'"""}
    p = PraatLoader(additional_scripts=scripts)
    distance = p.run_script('mfcc_distance.praat',filename_one, filename_two)
    return float(distance)

def spectral_distance(filename_one, filename_two):
    scripts = {'spec_distance.praat':"""
form Variables
    sentence firstfile
    sentence secondfile
endform

Read from file... 'firstfile$'
first = selected()

Read from file... 'secondfile$'
second = selected()

select first
To Spectrogram... 0.005 8000 0.002 20 Gaussian
first_spec = selected()

select second
To Spectrogram... 0.005 8000 0.002 20 Gaussian
second_spec = selected()

select first_spec
plus second_spec
To DTW... 1 1 no restriction
spec_dist = Get distance (weighted)

echo 'spec_dist'"""}
    p = PraatLoader(additional_scripts=scripts)
    distance = p.run_script('spec_distance.praat',filename_one, filename_two)
    return float(distance)
