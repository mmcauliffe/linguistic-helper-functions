from linghelper.phonetics.praat import PraatLoader
from linghelper.phonetics.praat.helper import to_time_based_dict

from scipy.interpolate import interp1d

from numpy import vstack,array
    
def interpolate_pitch(pitch_track):
    defined_keys = [k for k in sorted(pitch_track.keys()) if pitch_track[k]['Pitch'] != '--undefined--']
    x = array(defined_keys)
    y = array([ pitch_track[k]['Pitch'] for k in defined_keys])
    if len(x) == 0:
        return None
    times = list(filter(lambda z: z >= min(x) and z <= max(x),defined_keys))
    f = interp1d(x,y)
    return f(times),min(x),max(x)

def get_intensity_spline(intensity_track):
    y = array([ intensity_track[k]['Intensity'] for k in sorted(intensity_track.keys()) if intensity_track[k]['Intensity'] != '--undefined--'])
    return y
    
    
def to_pitch(filename,time_step):
    p = PraatLoader()
    output = p.run_script('pitch.praat', filename,time_step)
    try:
        pitch = to_time_based_dict(output)
    except IndexError:
        return None
    pitch_spline = interpolate_pitch(pitch)
    if pitch_spline is None:
        return None
    return pitch_spline.T
    
def to_intensity(filename,time_step):
    p = PraatLoader()
    output = p.run_script('intensity.praat', filename,time_step)
    intensity = to_time_based_dict(output)
    intensity_spline = get_intensity_spline(intensity)
    return intensity_spline.T
    
def to_prosody(filename,time_step):
    scripts = {'prosody.praat':"""
        form Variables
            sentence filename
            real timestep
        endform


        Read from file... 'filename$'
        
        name$ = selected$("Sound")

        To Pitch (ac)... 'timestep' 75.0 15 yes 0.03 0.45 0.01 0.35 0.14 600.0
        
        select Sound 'name$'
        
        To Intensity... 75 0.005 yes
        
        frames = Get number of frames

        output$ = "Time"+tab$+"Pitch"+tab$+"Intensity"+newline$
        
        
        for f from 1 to frames
            select Pitch 'name$'
            t = Get time from frame number... 'f'
            t$ = fixed$(t, 3)
            pitch = Get value in frame... 'f' Hertz
            pitch$ = fixed$(pitch, 2)
            select Intensity 'name$'
            intensity = Get value at time... 't' Cubic
            intensity$ = fixed$(intensity, 2)
            output$ = output$+t$+tab$+pitch$+tab$+intensity$+newline$
        endfor

        echo 'output$'"""}
    p = PraatLoader(additional_scripts=scripts)
    output = p.run_script('prosody.praat', filename,time_step)
    prosody = to_time_based_dict(output)
    pitch_spline,defined_min,defined_max = interpolate_pitch(prosody)
    intensity = {k:v for k,v in prosody.items() if k >= defined_min and k <= defined_max}
    intensity_spline = get_intensity_spline(intensity)
    prosody = vstack((pitch_spline,intensity_spline))
    return prosody.T
    
    
