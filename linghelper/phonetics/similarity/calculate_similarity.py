from linghelper.phonetics.similarity.envelope import calc_envelope, correlate_envelopes
from linghelper.phonetics.similarity.spectral import mfcc_distance,spectral_distance
from linghelper.phonetics.similarity.linguistic_cues import pitch_distance, intensity_distance
import math


def phonetic_similarity(path_mapping,
                            sim_type = 'envelope',
                            num_bands = 8,
                            freq_lims = (80,7800),
                            erb = False,
                            praatpath='praat'):
    output_values = []
    total_mappings = len(path_mapping)
    if sim_type == 'envelope':
        envelope_cache = {}
        for i,pm in enumerate(path_mapping):
            if i % 10 == 0:
                print('processed file %d of %d' % (i,total_mappings))
            for filepath in pm:
                if filepath not in envelope_cache:
                    envelope_cache[filepath] = calc_envelope(filepath,num_bands,freq_lims,erb)

            if len(pm) == 2:
                sim_val = correlate_envelopes(envelope_cache[pm[0]],envelope_cache[pm[1]])
                output_values.append([pm[0],pm[1],sim_val])
            elif len(pm) == 3:
                sim_val1 = correlate_envelopes(envelope_cache[pm[0]],envelope_cache[pm[1]])
                sim_val2 = correlate_envelopes(envelope_cache[pm[1]],envelope_cache[pm[2]])
                output_values.append([pm[0],pm[1],pm[2], sim_val1,sim_val2])
    elif 'dct' in sim_type:
        if sim_type == 'pitch_dct':
            praat_func = pitch_distance
        elif sim_type == 'intensity_dct':
            praat_func = intensity_distance
        for i,pm in enumerate(path_mapping):
            if i % 10 == 0:
                print('processed file %d of %d' % (i,total_mappings))
            if len(pm) == 2:
                dist_val = praat_func(pm[0],pm[1],praatpath)
                if dist_val is None:
                    continue
                sim_val = 1 / math.log(dist_val)
                output_values.append([pm[0],pm[1],sim_val])
            elif len(pm) == 3:
                dist_val1 = praat_func(pm[0],pm[1],praatpath)
                if dist_val1 is None:
                    continue
                sim_val1 = 1 / math.log(dist_val1)

                dist_val2 = praat_func(pm[1],pm[2],praatpath)
                if dist_val2 is None:
                    continue
                sim_val2 = 1 / math.log(dist_val2)
                output_values.append([pm[0],pm[1],pm[2],sim_val1,sim_val2])
    else:

        if sim_type == 'spectral_dtw':
            spec_max = freq_lims[1]
            praat_func = spectral_distance
        elif sim_type == 'mfcc_dtw':
            spec_max = 2595 * math.log10(1+ (freq_lims[1]/700))
            praat_func = mfcc_distance
        for i,pm in enumerate(path_mapping):
            if i % 10 == 0:
                print('processed file %d of %d' % (i,total_mappings))
            if len(pm) == 2:
                dist_val = praat_func(pm[0],pm[1],spec_max,praatpath)
                sim_val = 1 / math.log(dist_val)
                output_values.append([pm[0],pm[1],sim_val])
            elif len(pm) == 3:
                dist_val1 = praat_func(pm[0],pm[1],spec_max,praatpath)
                sim_val1 = 1 / math.log(dist_val1)

                dist_val2 = praat_func(pm[1],pm[2],spec_max,praatpath)
                sim_val2 = 1 / math.log(dist_val2)

                output_values.append([pm[0],pm[1],pm[2],sim_val1,sim_val2])
    return output_values

