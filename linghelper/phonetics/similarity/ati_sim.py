import os
import subprocess
import sys
import csv

sys.path.append('/home/michael/dev/Linguistics/linguistic-helper-functions')

from linghelper.phonetics.similarity.calculate_similarity import phonetic_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATTERNS = {'Model':'(?P<Gender>\w)_subj(?P<Number>\d+)_(?P<Vowel>\w)_(?P<Word>\w+)',
            'Shadower_baseline':'Subject(?P<Number>\d+)-(?P<Gender>\w+)-baseline-(?P<Vowel>\w)-(?P<Word>\w+)',
            'Shadower_shadowed':'Subject(?P<ShadowerNumber>\d+)-(?P<ShadowerGender>\w+)-shadow-(?P<ModelGender>\w)_subj(?P<ModelNumber>\d+)-(?P<VoiceType>\w+)_(?P<Region>\w+)-(?P<Vowel>\w)-(?P<Word>\w+)'}

VOICETYPE = {'225': 'mostattractive_CAL',
                '243':'leasttypical_CAL',
                '262':'mosttypical_CAL',
                '278':'leastattractive_CAL',
                '274':'mosttypical_CAL',
                '304':'leastattractive_CAL',
                '316':'leasttypical_CAL',
                '321':'mostattractive_CAL'}

ati_dir = '/media/Data/Corpora/ATI'
model_dir = os.path.join(ati_dir,'Model')
shadower_dir = os.path.join(ati_dir,'Shadowers')
male_models = os.listdir(os.path.join(model_dir,'Male'))
female_models = os.listdir(os.path.join(model_dir,'Female'))
models = list(map(lambda x: (x,'Male'),male_models))
models += list(map(lambda x: (x,'Female'),female_models))
male_shadowers = os.listdir(os.path.join(shadower_dir,'Male'))
female_shadowers = os.listdir(os.path.join(shadower_dir,'Female'))
shadowers = list(map(lambda x: (x,'Male'),male_shadowers))
shadowers += list(map(lambda x: (x,'Female'),female_shadowers))
numBands = 8
words = [('a','cot'),
            ('a','pod'),
            ('a','sock'),
            ('a','sod'),
            ('a','tot'),
            ('i','deed'),
            ('i','key'),
            ('i','peel'),
            ('i','teal'),
            ('i','weave'),
            ('u','boot'),
            ('u','dune'),
            ('u','hoop'),
            ('u','toot'),
            ('u','zoo')]

def extract_sound_file_info(filename,pattern):
    m = re.match(pattern,filename)
    info = m.groupdict()
    for k in info:
        if 'Gender' not in k:
            continue
        if len(info[k]) > 1:
            continue
        if info[k] == 'm':
            info[k] = 'male'
        elif info[k] == 'f':
            info[k] = 'female'
    return info


def lookup_model_wav(model_number,model_gender,vowel,word,ati_dir):
    gender = 'f'
    if model_gender == 'Male':
        gender = 'm'
    wav_path = '%s_subj%s_%s_%s.wav' % (gender, model_number, vowel, word)
    speaker_dir = os.path.join(ati_dir,'Model',model_gender,model_number)
    files = os.listdir(speaker_dir)
    return os.path.join(speaker_dir,wav_path)

def lookup_shadower_wav(shadower_number,shadower_gender,production,vowel,word,ati_dir,model_number=None,model_gender=None):
    shadower_string = ''
    if model_number:
        shadower_string = '-%s_subj%s-%s' % (model_gender[0].lower(),model_number,VOICETYPE[model_number])
        prod = '%s_%s' % (production,model_gender.lower())
        production_dir = os.path.join(ati_dir,'Shadowers',shadower_gender,shadower_number,prod,model_number)
    else:
        production_dir = os.path.join(ati_dir,'Shadowers',shadower_gender,shadower_number,production)
    wav_path = 'Subject%s-%s-%s%s-%s-%s.wav' % (shadower_number,shadower_gender.lower(),
                                                production.lower(),shadower_string,vowel,word)

    files = os.listdir(production_dir)
    return os.path.join(production_dir,wav_path)

def generate_path_mapping():
    path_mapping = []
    for m in models:
        print(m)
        for w in words:
            print(w)
            model_path = lookup_model_wav(m[0],m[1],w[0],w[1],ati_dir)
            if not os.path.isfile(model_path):
                continue
            for s in shadowers:
                baseline_path = lookup_shadower_wav(s[0],s[1],'Baseline',w[0],w[1],ati_dir)
                
                if not os.path.isfile(baseline_path):
                    continue
                shadowed_path = lookup_shadower_wav(s[0],s[1],'Shadow',w[0],w[1],ati_dir,model_number=m[0],model_gender=m[1])
                
                if not os.path.isfile(shadowed_path):
                    continue
                path_mapping.append((baseline_path,model_path,shadowed_path))
    return path_mapping

if __name__ == '__main__':
    path_mapping = generate_path_mapping()
    print('calcing pitch similarities')
    pitch_sims = phonetic_similarity(path_mapping,sim_type='pitch_dct',praatpath='/home/michael/Documents/Linguistics/Tools/Praat/praat')
    print(len(pitch_sims))
    print('calcing intensity similarities')
    intensity_sims = phonetic_similarity(path_mapping,sim_type='intensity_dct',praatpath='/home/michael/Documents/Linguistics/Tools/Praat/praat')
    print(len(intensity_sims))
    #envelope_sims = phonetic_similarity(path_mapping)
    #spectral_sims = phonetic_similarity(path_mapping,sim_type = 'spectral_dtw',praatpath='/home/michael/Documents/Linguistics/Tools/Praat/praat')
    #mfcc_sims = phonetic_similarity(path_mapping,sim_type = 'mfcc_dtw',praatpath='/home/michael/Documents/Linguistics/Tools/Praat/praat')
    with open(os.path.join(BASE_DIR,'ati_outputAllSims.txt'),'w') as f:
        csvw = csv.writer(f,delimiter='\t')
        csvw.writerow(['Baseline_filename','Model_filename','Shadowed_filename',
                        #'Base_to_Model_env_sim',
                        #'Shad_to_Model_env_sim',
                        #'Base_to_Model_spec_sim',
                        #'Shad_to_Model_spec_sim',
                        #'Base_to_Model_mfcc_sim',
                        #'Shad_to_Model_mfcc_sim',
                        'Base_to_Model_pitch_sim',
                        'Shad_to_Model_pitch_sim',
                        'Base_to_Model_intensity_sim',
                        'Shad_to_Model_intensity_sim',])
        for i in range(len(envelope_sims)):
            row = [os.path.split(envelope_sims[i][0])[1],
                    os.path.split(envelope_sims[i][1])[1],
                    os.path.split(envelope_sims[i][2])[1],
                    #envelope_sims[i][3],envelope_sims[i][4],
                    #spectral_sims[i][3],spectral_sims[i][4],
                    #mfcc_sims[i][3],mfcc_sims[i][4],
                    pitch_sims[i][3],pitch_sims[i][4],
                    intensity_sims[i][3],intensity_sims[i][4],
                    ]
            csvw.writerow(row)
