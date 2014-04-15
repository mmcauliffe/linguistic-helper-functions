from linghelper.phonetics.praat import PraatLoader
from linghelper.phonetics.praat.helper import to_time_based_dict

from scipy.spatial.distance import euclidean
from scipy.interpolate import interp1d
from scipy.fftpack import dct

import numpy as np
    
def interpolate_pitch(pitch_track):
    x = np.array([ k for k in sorted(pitch_track.keys()) if pitch_track[k]['Pitch'] != '--undefined--'])
    y = np.array([ pitch_track[k]['Pitch'] for k in sorted(pitch_track.keys()) if pitch_track[k]['Pitch'] != '--undefined--'])
    if len(x) == 0:
        return None
    times = list(filter(lambda z: z >= min(x) and z <= max(x),sorted(pitch_track.keys())))
    f = interp1d(x,y)
    return f(times)

def get_intensity_spline(intensity_track):
    y = np.array([ intensity_track[k]['Intensity'] for k in sorted(intensity_track.keys()) if intensity_track[k]['Intensity'] != '--undefined--'])
    return y
    
    
def to_pitch(filename):
    p = PraatLoader(praatpath=praatpath)
    output = p.run_script('pitch.praat', filename)
    try:
        pitch = to_time_based_dict(output)
    except IndexError:
        return None
    pitch_spline = interpolate_pitch(pitch)
    if pitch_spline is None:
        return None
    return pitch_spline.T
    
def to_intensity(filename):
    p = PraatLoader(praatpath=praatpath)
    output = p.run_script('intensity.praat', filename)
    intensity = to_time_based_dict(output)
    intensity_spline = get_intensity_spline(intensity)
    return intensity_spline.T