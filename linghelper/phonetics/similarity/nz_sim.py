import os
import subprocess
import sys
import csv

sys.path.append('/home/michael/dev/Linguistics/linguistic-helper-functions')
sys.path.append('/home/michael/dev/Linguistics/python-praat-scripts')
from linghelper.phonetics.similarity.envelope import envelope_similarity
from linghelper.phonetics.similarity.spectral import mfcc_distance,spectral_distance


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.normpath('/home/michael/dev/Data/NZDiph/AUModelTokens')
NZ_DIR = os.path.normpath('/home/michael/dev/Data/NZDiph/NZSoundFiles')

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

if __name__ == '__main__':
    with open(os.path.join(BASE_DIR,'output.txt'),'w') as f:
        csvw = csv.writer(f,delimiter='\t')
        csvw.writerow(['Shadower_number','Block'
                        'Word','shad_to_mod_env_sim','base_to_mod_env_sim',
                        #'mfcc_shad_to_mod','mfcc_mod_to_shad',
                        #'spec_shad_to_mod','spec_mod_to_shad',
                        #'mfcc_base_to_mod','mfcc_mod_to_base',
                        #'spec_base_to_mod','spec_mod_to_base'
                        ])
        for s in Shadowers:
            print(s)
            for w in Words:
                print(w)
                for b in Block.keys():
                    if b == 'Baseline':
                        continue
                    print(b)
                    shad_path = get_shadower_path(w,s,b)
                    model_path = get_model_path(w)
                    base_path = get_shadower_path(w,s,'Baseline')

                    if os.path.isfile(shad_path) and os.path.isfile(model_path) and os.path.isfile(base_path):
                        shad_to_mod_env_sim = envelope_similarity(shad_path,model_path,num_bands=16)
                        base_to_mod_env_sim = envelope_similarity(base_path,model_path,num_bands=16)
                        #mfcc_shad_to_mod = mfcc_distance(shad_path,model_path)
                        #mfcc_mod_to_shad = mfcc_distance(model_path,shad_path)
                        #spec_shad_to_mod = spectral_distance(shad_path,model_path)
                        #spec_mod_to_shad = spectral_distance(model_path,shad_path)

                        #mfcc_base_to_mod = mfcc_distance(base_path,model_path)
                        #mfcc_mod_to_base = mfcc_distance(model_path,base_path)
                        #spec_base_to_mod = spectral_distance(base_path,model_path)
                        #spec_mod_to_base = spectral_distance(model_path,base_path)
                    else:
                        shad_to_env_sim = 'NA'
                        base_to_env_sim = 'NA'
                        #mfcc_shad_to_mod = 'NA'
                        #mfcc_mod_to_shad ='NA'
                        #spec_shad_to_mod = 'NA'
                        #spec_mod_to_shad = 'NA'

                        #mfcc_base_to_mod = 'NA'
                        #mfcc_mod_to_base ='NA'
                        #spec_base_to_mod = 'NA'
                        #spec_mod_to_base = 'NA'
                    csvw.writerow([s,b,w,shad_to_mod_env_sim,base_to_mod_env_sim,
                            #mfcc_shad_to_mod,mfcc_mod_to_shad,
                            #spec_shad_to_mod,spec_mod_to_shad,
                            #mfcc_base_to_mod,mfcc_mod_to_base,
                            #spec_base_to_mod,spec_mod_to_base
                            ])
