import sys
sys.path.append('/home/michael/dev/Linguistics/linguistic-helper-functions')
sys.path.append('/home/michael/dev/Linguistics/python-praat-scripts')

from scipy.spatial.distance import euclidean

from praatinterface import PraatLoader

from vowels.formants import analyze_vowel
from helper import DCT, UnDCT, get_intensity, get_pitch, to_ordered_list



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
    return distance

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
    return distance

def formant_distance(file_one_info,file_two_info, method = 'DCT'):
    p = PraatLoader()
    vowel_one = filename_one.replace('.wav','-vowel.wav')
    analyze_vowel('extract.praat', file_one_info['filename'], file_one_info['beg'], file_one_info['end'])

def pitch_distance(filename_one, filename_two):
    p = PraatLoader()

def intensity_distance(filename_one, filename_two, method = 'DCT'):
    int_one = get_intensity(filename_one)
    int_two = get_intensity(filename_two)
    if method == 'DCT':
        dct_one = DCT(to_ordered_list(int_one))[:3]
        dct_two = DCT(to_ordered_list(int_two))[:3]
        dist = euclidean(dct_one,dct_two)
    return dist



if __name__ == '__main__':
    #file_one = '/home/michael/dev/LingToolsWebsite/Media/Temp/Buckeye-4505.wav'
    #file_two = '/home/michael/dev/LingToolsWebsite/Media/Temp/Buckeye-1508.wav'
    file_one = {
                'filename':'/home/michael/Documents/Grad/PhD/MollyLab/NZDiph/Scripting/AUModelTokens/spare.wav',
                'vowel': 'EY',
                'beg': 0.208,
                'end': 0.421,
                }
    file_two = {
                'filename':'/home/michael/Documents/Grad/PhD/MollyLab/NZDiph/Scripting/AUModelTokens/spear.wav',
                'vowel': 'IY',
                'beg': 0.199,
                'end': 0.358,
                }
    print(intensity_distance(file_one['filename'],file_two['filename']))
    print(spectral_distance(file_one['filename'],file_two['filename']))
    print(mfcc_distance(file_one['filename'],file_two['filename']))

