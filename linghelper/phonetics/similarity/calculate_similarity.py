from linghelper.phonetics.representations.amplitude_envelope import to_envelopes
from linghelper.phonetics.representations.mfcc import to_mfcc,freq_to_mel
from linghelper.phonetics.representations.prosody import to_pitch, to_intensity
from linghelper.distance.dtw import dtw_distance
from linghelper.distance.xcorr import xcorr_distance
from linghelper.distance.dct import dct_distance

import math



def phonetic_similarity(path_mapping,
                            representation = 'envelope',
                            match_algorithm = 'xcorr',
                            num_bands = 8,
                            freq_lims = (80,7800),
                            erb = False,
                            words=None,
                            vowels=None,
                            output_sim = True):
    output_values = []
    total_mappings = len(path_mapping)
    cache = {}
    if representation == 'envelope':
        for i,pm in enumerate(path_mapping):
            if i % 50 == 0:
                print('Mapping %d of %d converted to envelopes' % (i,total_mappings))
            for filepath in pm:
                if filepath not in cache:
                    cache[filepath] = calc_envelope(filepath,num_bands,freq_lims,erb)
    elif representation == 'mfcc':
        maxMel = freq_to_mel(freq_lims[1])
        for i,pm in enumerate(path_mapping):
            if i % 50 == 0:
                print('Mapping %d of %d converted to MFCCs' % (i,total_mappings))
            for filepath in pm:
                if filepath not in cache:
                    cache[filepath] = to_mfcc(filepath,20,0.015,0.005,maxMel)
    elif representation == 'pitch':
        for i,pm in enumerate(path_mapping):
            if i % 50 == 0:
                print('Mapping %d of %d converted to pitch' % (i,total_mappings))
            for filepath in pm:
                if filepath not in cache:
                    cache[filepath] = to_pitch(filepath)
    elif representation == 'intensity':
        for i,pm in enumerate(path_mapping):
            if i % 50 == 0:
                print('Mapping %d of %d converted to intensity' % (i,total_mappings))
            for filepath in pm:
                if filepath not in cache:
                    cache[filepath] = to_intensity(filepath)
                    
    if match_algorithm == 'xcorr':
        dist_func = xcorr_distance
    elif match_algorithm == 'dtw':
        dist_func = dtw_distance
    elif match_algorithm == 'dct':
        dist_func = dct_distance
        
    for i,pm in enumerate(path_mapping):
        if i % 50 == 0:
            print('Mapping %d of %d %sed' % (i,total_mappings,match_algorithm))

        if len(pm) == 2:
            dist_val = dist_func(cache[pm[0]],cache[pm[1]])
            if output_sim:
                dist_val = 1/math.pow(math.e,dist_val)
            output_values.append([pm[0],pm[1],dist_val])
        elif len(pm) == 3:
            dist_val1 = dist_func(cache[pm[0]],cache[pm[1]])
            dist_val2 = dist_func(cache[pm[2]],cache[pm[1]])
            if output_sim:
                dist_val1 = 1/math.pow(math.e,dist_val1)
                dist_val2 = 1/math.pow(math.e,dist_val2)
            output_values.append([pm[0],pm[1],pm[2], dist_val1,dist_val2])
    
    return output_values

