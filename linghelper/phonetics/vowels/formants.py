import numpy as np
import os
import sys
from scipy.spatial.distance import mahalanobis

from linghelper.phonetics.praat import PraatLoader

from .mahalanobis import MEANS,COVS

from linghelper.phonetics.helper import smooth, DCT

A2P = {'AA':'5', 'AE':'3', 'AH':'6', 'AO':'53', 'AW':'42', 'AY':'41', 'EH':'2', 'ER':'94', 'EY':'21', 'IH':'1', 'IY':'11', 'OW':'62', 'OY':'61', 'UH':'7', 'UW':'72'}
A2P_FINAL = {'IY':'12', 'EY':'22', 'OW':'63'}
A2P_R = {'EH':'2', 'AE':'3', 'IH':'14', 'IY':'14', 'EY':'24', 'AA':'44', 'AO':'64', 'OW':'64', 'UH':'74', 'UW':'74', 'AH':'6', 'AW':'42', 'AY':'41', 'OY':'61'}

class FormantTrack(object):
    def __init__(self,tracks,point = 'third'):
        self.tracks = tracks
        beg = min(tracks.keys())
        end = max(tracks.keys())
        duration = end - beg
        self.vdur = duration
        third = (duration/3.0)+beg
        halfway = duration / 2.0
        if point == 'maxF1':
            measurement_point = max(filter(
                            lambda x: x < beg + halfway and 'F1' in tracks[x] and
                                    'F2' in tracks[x], tracks.keys()
                                ),key = lambda x: tracks[x]['F1'])
        elif point == 'beforemaxF1':
            measurement_point = max(filter(
                            lambda x: x < beg + halfway and 'F1' in tracks[x] and
                                    'F2' in tracks[x], tracks.keys()
                                ),key = lambda x: tracks[x]['F1'])
            half = ((measurement_point-beg)/2.0)+beg
            measurement_point = min(tracks.keys(),key=lambda x: abs(x-half))
        elif point == 'beginning':
            measurement_point = beg
        else:
            t = filter(lambda x: all(k in tracks[x] for k in ['F1','F2']),tracks.keys())
            measurement_point = min(t,key=lambda x: abs(x-third))
        self.point = measurement_point

    def get_point_measurement(self,keys = ['F1','F2','B1','B2'],return_dict = False):
        if return_dict:
            return {k: self.tracks[self.point][k] for k in keys if k in self.tracks[self.point]}
        return [self.tracks[self.point][x] for x in keys]

    def get_track(self,track_name):
        return [self.tracks[x][track_name]
                            for x in sorted(self.tracks.keys())
                                if track_name in self.tracks[x]]

    def get_vdur(self):
        return self.vdur

    def get_DCT(self,track_name,num_coeff=3,return_dict = False):
        dct = DCT(self.get_track(track_name),num_coeff)
        if return_dict:
            try:
                output = {'%sC%d' % (track_name,c+1): dct[c] for c in range(num_coeff)}
            except IndexError:
                output = {'%sC%d' % (track_name,c+1): None for c in range(num_coeff)}
            return output
        return dct

def formant_tracks(filename, n, max_formant, praat = None):
    if not praat:
        praat = PraatLoader(debug=True)
    text = praat.run_script('formant_list.praat', filename, n, max_formant)
    return praat.read_praat_out(text)


def calc_distance(tracks, means, covs,remeasure):
    f_point = tracks.get_point_measurement()
    if remeasure:
        f_point.append(tracks.get_vdur())
    c = np.matrix(covs).I
    dist = mahalanobis(f_point,means, c)
    return dist

def get_formant_tracks(filename, means = None, covs = None,
                        max_formant = 5000, point = 'third',
                        remeasure = False):
    best = (None,None)
    n_current = 0
    for n in range(3,7):
        t = formant_tracks(filename, n, max_formant)
        tracks = FormantTrack(t,point)
        #tracks = smooth(tracks, 12)
        if means:
            distance = calc_distance(tracks,means,covs,remeasure)
            if not best[0] or best[0] > distance:
                best = (distance,tracks)
                n_current = n
        elif n == 5:
            best = None,tracks
    return best[1]

def get_relevant_features(foll_seg, prec_seg):
    if prec_seg in set(['T','D','DX','EN','EL','N','L','R','S','Z']):
        prec_seg = 'alveolar'
    else:
        prec_seg = ''
    if foll_seg in set(['R','AXR']):
        foll_seg = 'rhotic'
    elif foll_seg != '':
        foll_seg = 'other'
    return foll_seg, prec_seg

def get_vowel_code(vowel,foll_seg,prec_seg):
    vowel = vowel.upper()
    point = 'third'
    if vowel is None:
        return '', point
    if vowel.endswith('N'):
        foll_seg = 'N'
        vowel = vowel[:-1]
    foll_seg,prec_seg = get_relevant_features(foll_seg, prec_seg)
    if vowel == 'UW' and prec_seg == 'alveolar':
        pc = '73'
    elif foll_seg == 'rhotic' and vowel != 'ER':
        pc = A2P_R[vowel]
    elif vowel in ['IY','EY','OW'] and foll_seg == '':
        pc = A2P_FINAL[vowel]
    else:
        pc = A2P[vowel]
    return pc,point


def get_speaker_means(measurements):
    """
    measurements should be a dict of keys which are tuples of (vowel, foll_seg, prec_seg)
    and items which are lists of dictionarys with 'F1','F2','B1','B2', and 'VDur' as keys
    """
    means = {}
    covs = {}
    by_vowel_code = {}
    for key, value in measurements.items():
        vowel_code, point = get_vowel_code(*key)
        if vowel_code not in by_vowel_code:
            by_vowel_code[vowel_code] = []
        for y in value:
            by_vowel_code[vowel_code].append([ y[x] for x in ['F1','F2','B1','B2','VDur']])
    for key,value in by_vowel_code.items():
        #mat = [value[x] for x in ['F1','F2','B1','B2','VDur'] for y in value]
        value = np.array(value)
        cov = np.cov(value,rowvar=0)

        ms = [np.mean(value[:,x]) for x in range(value.shape[1])]
        means[key] = ms
        covs[key] = cov
    return means, covs


def analyze_vowel(filename, vowel=None, foll_seg=None, prec_seg=None,
                    speaker_gender=None,method='mahalanobis', means=None,covs=None):
    vowel_code,point = get_vowel_code(vowel,foll_seg, prec_seg)

    if speaker_gender in ['f','F','female']:
        max_formant = 5500
    else:
        max_formant = 5000
    if method == 'mahalanobis':
        if not means and not covs:
            m = MEANS[vowel_code]
            c = COVS[vowel_code]
            remeasure = False
        else:
            m = means[vowel_code]
            c = covs[vowel_code]
            remeasure = True
        tracks = get_formant_tracks(filename,means=m,covs=c,max_formant=max_formant,point=point,remeasure=remeasure)
    else:
        tracks = get_formant_tracks(filename,max_formant=max_formant,point=point)
    return tracks
