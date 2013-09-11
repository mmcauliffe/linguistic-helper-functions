import numpy as np
from scipy.spatial.distance import mahalanobis

from praatinterface import PraatLoader

from linghelper.phonetics.vowels.mahalanobis import MEANS,COVS

from linghelper.phonetics.helper import smooth

A2P = {'AA':'5', 'AE':'3', 'AH':'6', 'AO':'53', 'AW':'42', 'AY':'41', 'EH':'2', 'ER':'94', 'EY':'21', 'IH':'1', 'IY':'11', 'OW':'62', 'OY':'61', 'UH':'7', 'UW':'72'}
A2P_FINAL = {'IY':'12', 'EY':'22', 'OW':'63'}
A2P_R = {'EH':'2', 'AE':'3', 'IH':'14', 'IY':'14', 'EY':'24', 'AA':'44', 'AO':'64', 'OW':'64', 'UH':'74', 'UW':'74', 'AH':'6', 'AW':'42', 'AY':'41', 'OY':'61'}

def formant_tracks(filename, n, max_formant, praat = None):
    if not praat:
        praat = PraatLoader()
    text = praat.run_script('formants.praat', filename, n, max_formant)
    return praat.read_praat_out(text)

def get_measurement_at_point(tracks, point):
    beg = min(tracks.keys())
    end = max(tracks.keys())
    duration = end - beg
    third = (duration/3.0)+beg
    halfway = duration / 2.0
    if point == 'maxF1':
        measurement_point = max(filter(
                        lambda x: x < beg + halfway and 'F1' in tracks[x] and 'F2' in tracks[x], tracks.keys()
                            ),key = lambda x: tracks[x]['F1'])
    elif point == 'beforemaxF1':
        measurement_point = max(filter(
                        lambda x: x < beg + halfway and 'F1' in tracks[x] and 'F2' in tracks[x], tracks.keys()
                            ),key = lambda x: tracks[x]['F1'])
        half = ((measurement_point-beg)/2.0)+beg
        measurement_point = min(tracks.keys(),key=lambda x: abs(x-half))
    elif point == 'beginning':
        measurement_point = beg
    else:
        measurement_point = min(tracks.keys(),key=lambda x: abs(x-third))
    f_point = np.array([tracks[measurement_point][x] for x in ['F1','F2','B1','B2']])
    return f_point

def calc_distance(tracks, means, cov, point):
    f_point = get_measurement_at_point(tracks, point)
    dist = mahalanobis(f_point,means, cov.getI())
    return dist

def get_formant_tracks(filename, means = None, cov = None, max_formant = 5000, point = 'third'):
    best = (None,None)
    n_current = 0
    for n in range(3,7):
        tracks = formant_tracks(filename, n, max_formant)
        tracks = smooth(tracks, 12)
        if means:
            distance = calc_distance(tracks,means,cov,point)
            if not best[0] or best[0] > distance:
                best = (distance,tracks)
                n_current = n
        elif n == 5:
            best = None,tracks
    point_measure = get_measurement_at_point(best[1], point)
    return best[1],point_measure

def get_vowel_code(vowel,foll_seg,prec_seg):
    if vowel == 'UW' and prec_seg == 'alveolar':
        pc = '73'
    elif foll_seg == 'rhotic' and vowel != 'ER':
        pc = A2P_R[vowel]
    elif vowel in ['IY','EY','OW'] and foll_seg:
        pc = A2P_FINAL[vowel]
    else:
        pc = A2P[vowel]
    return pc


def get_speaker_means(measurements):
    for key, value in measurements.items():
        vowel_code = get_vowel_code(*key)


def analyze_vowel(filename, vowel=None, foll_seg=None, prec_seg=None,
                    speaker_gender=None, measurement='mahalanobis', means=None,covs=None):
    if vowel:
        vowel_code,point = get_vowel_code(vowel,foll_seg, prec_seg)
    if speaker_gender in ['f','F','female']:
        max_formant = 5500
    else:
        max_formant = 5000
    if measurement == 'mahalanobis':
        if not means and not covs:
            m = MEANS[vowel_code]
            c = COVS[vowel_code]
        track,point = get_formant_tracks(filename,means=m,covs=c,max_formant=max_formant,point=point)
    else:
        track, point = get_formant_tracks(filename,max_formant=max_formant,point=point)
    return track,point
