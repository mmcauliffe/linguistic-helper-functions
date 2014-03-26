from linghelper.phonetics.praat import PraatLoader

from scipy.spatial.distance import euclidean
from scipy.interpolate import interp1d
from scipy.fftpack import dct

import numpy as np

import re

def to_time_based_dict(praat_output,remove_undefined = False):
    lines = praat_output.splitlines()
    head = re.sub('[(]\w+[)]','',lines.pop(0))
    head = head.split("\t")[1:]
    output = {}
    for l in lines:
        if '\t' in l:
            line = l.split("\t")
            time = line.pop(0)
            values = {}
            for j in range(len(line)):
                if remove_undefined and line[j] == '--undefined--':
                    continue
                v = line[j]
                if v != '--undefined--':
                    v = float(v)
                values[head[j]] = v
            if values:
                output[float(time)] = values
    return output
    
def interpolate_pitch(pitch_track):
    x = np.array([ k for k in sorted(pitch_track.keys()) if pitch_track[k]['Pitch'] != '--undefined--'])
    y = np.array([ pitch_track[k]['Pitch'] for k in sorted(pitch_track.keys()) if pitch_track[k]['Pitch'] != '--undefined--'])
    if len(x) == 0:
        return None
    times = list(filter(lambda z: z >= min(x) and z <= max(x),sorted(pitch_track.keys())))
    f = interp1d(x,y)
    return f(times)



def pitch_distance(filename_one, filename_two,praatpath,norm_level = True):
    p = PraatLoader(praatpath=praatpath)
    output = p.run_script('pitch.praat', filename_one)
    try:
        pitch_one = to_time_based_dict(output)
    except IndexError:
        print(filename_one)
    pitch_one_spline = interpolate_pitch(pitch_one)
    if pitch_one_spline is None:
        return None
    pitch_one_dct = dct(pitch_one_spline,norm='ortho')
    if norm_level:
        pitch_one_dct = pitch_one_dct[1:]
    pitch_one_dct = pitch_one_dct[0:3]
    
    output = p.run_script('pitch.praat', filename_two)
    try:
        pitch_two = to_time_based_dict(output)
    except IndexError:
        print(filename_two)
    pitch_two_spline = interpolate_pitch(pitch_two)
    if pitch_two_spline is None:
        return None
    pitch_two_dct = dct(pitch_two_spline,norm='ortho')
    if norm_level:
        pitch_two_dct = pitch_two_dct[1:]
    pitch_two_dct = pitch_two_dct[0:3]
    
    return euclidean(pitch_one_dct,pitch_two_dct)
    
def intensity_distance(filename_one, filename_two,praatpath,norm_level = True):
    p = PraatLoader(praatpath=praatpath)
    
    output = p.run_script('intensity.praat', filename_one)
    intensity_one = to_time_based_dict(output)
    intensity_one_dct = dct(intensity_one,norm='ortho')
    if norm_level:
        intensity_one_dct = intensity_one_dct[1:]
    intensity_one_dct = intensity_one_dct[0:3]
    
    output = p.run_script('intensity.praat', filename_two)
    intensity_two = to_time_based_dict(output)
    intensity_two_dct = dct(intensity_two,norm='ortho')
    if norm_level:
        intensity_two_dct = intensity_two_dct[1:]
    intensity_two_dct = intensity_two_dct[0:3]
    
    return euclidean(intensity_one_dct,intensity_two_dct)
    
def formant_distance(filename_one, filename_two,praatpath,norm_level = True):
    pass
    
    
