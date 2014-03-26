import os
import subprocess
import sys
import csv

sys.path.append('/home/michael/dev/Linguistics/linguistic-helper-functions')

from linghelper.phonetics.similarity.calculate_similarity import phonetic_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.normpath('/media/Data/Corpora/NZDiph/AUModelTokens')
NZ_DIR = os.path.normpath('/media/Data/Corpora/NZDiph/NZSoundFiles')

Shadowers = ['s101','s102','s103','s104','s105','s106','s107','s109','s110',
            's111','s112','s113','s114','s115','s117','s118','s119',
            's120','s121','s122','s123','s124','s125','s126','s127','s128',
            's129','s130','s131','s132','s133',
            's134','s135','s136','s137',
            's138','s139','s140','s141','s142','s208']

Words = ['air','ear',
        'bare','beer',
        'dare', 'dear',
        'fare','fear',
        'hair','hear',
        'pair','peer',
        'rarely','really',
        'share','sheer',
        'spare','spear']

Block = {'Baseline':('','_baseline'),
        'Shadow1':('1','_shadowed1'),
        'Shadow2':('2','_shadowed2'),
        'PostTask':('3','_post')}

def get_shadower_path(word,shadower,production):
    opts = Block[production]
    for o in opts:
        path = os.path.join(NZ_DIR,'%s_%s%s.wav' %(shadower,word,o))
        if os.path.isfile(path):
            return path
    return path

def get_model_path(word):
    return os.path.join(MODEL_DIR,'%s.wav' % word)


def generate_path_mapping():
    path_mapping = []
    for s in Shadowers:
        print(s)
        for w in Words:
            model_path = get_model_path(w)
            if not os.path.isfile(model_path):
                continue
            print(w)
            for b in Block.keys():
                if b == 'Baseline':
                    continue
                print(b)
                shadowed_path = get_shadower_path(w,s,b)
                baseline_path = get_shadower_path(w,s,'Baseline')
                if not os.path.isfile(shadowed_path):
                    continue
                if not os.path.isfile(baseline_path):
                    continue
                path_mapping.append((baseline_path,model_path,shadowed_path))
    return path_mapping

if __name__ == '__main__':
    numBands = 8
    path_mapping = generate_path_mapping()
    print(len(path_mapping))
    pitch_sims = phonetic_similarity(path_mapping,sim_type='pitch_dct',praatpath='/home/michael/Documents/Linguistics/Tools/Praat/praat')
    intensity_sims = phonetic_similarity(path_mapping,sim_type='intensity_dct',praatpath='/home/michael/Documents/Linguistics/Tools/Praat/praat')
    spectral_sims = phonetic_similarity(path_mapping,sim_type = 'spectral_dtw',praatpath='/home/michael/Documents/Linguistics/Tools/Praat/praat')
    mfcc_sims = phonetic_similarity(path_mapping,sim_type = 'mfcc_dtw',praatpath='/home/michael/Documents/Linguistics/Tools/Praat/praat')
    envelope_sims = phonetic_similarity(path_mapping)
    print(len(envelope_sims))
    with open(os.path.join(BASE_DIR,'nz_outputAllSims.txt'),'w') as f:
        csvw = csv.writer(f,delimiter='\t')
        csvw.writerow(['Baseline_filename','Model_filename','Shadowed_filename',
                        'Base_to_Model_env_sim',
                        'Shad_to_Model_env_sim',
                        'Base_to_Model_spec_sim',
                        'Shad_to_Model_spec_sim',
                        'Base_to_Model_mfcc_sim',
                        'Shad_to_Model_mfcc_sim',
                        'Base_to_Model_pitch_sim',
                        'Shad_to_Model_pitch_sim',
                        'Base_to_Model_intensity_sim',
                        'Shad_to_Model_intensity_sim',])
        for i in range(len(envelope_sims)):
            row = [os.path.split(envelope_sims[i][0])[1],
                    os.path.split(envelope_sims[i][1])[1],
                    os.path.split(envelope_sims[i][2])[1],
                    envelope_sims[i][3],envelope_sims[i][4],
                    spectral_sims[i][3],spectral_sims[i][4],
                    mfcc_sims[i][3],mfcc_sims[i][4],
                    pitch_sims[i][3],pitch_sims[i][4],
                    intensity_sims[i][3],intensity_sims[i][4],
                    ]
            csvw.writerow(row)
