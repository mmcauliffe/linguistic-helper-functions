import os
import subprocess
import sys
import csv

sys.path.append('/home/michael/dev/Linguistics/linguistic-helper-functions')
sys.path.append('/home/michael/dev/Linguistics/python-praat-scripts')
from linghelper.phonetics.similarity.envelope import envelope_similarity,calc_envelope,envelope_match
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
    numBands = 8
    with open(os.path.join(BASE_DIR,'nz_output8BandInfo.txt'),'w') as f:
        csvw = csv.writer(f,delimiter='\t')
        #csvw.writerow(['Shadower_number','Block'
                        #'Word','shad_to_mod_env_sim','base_to_mod_env_sim',
                        ##'mfcc_shad_to_mod','mfcc_mod_to_shad',
                        ##'spec_shad_to_mod','spec_mod_to_shad',
                        ##'mfcc_base_to_mod','mfcc_mod_to_base',
                        ##'spec_base_to_mod','spec_mod_to_base'
                        #])
        csvw.writerow(['Baseline_filename','Shadowed_filename','Model_filename',
                        'Base_to_Model_env_sim',
                        'Shad_to_Model_env_sim']+ ['B%d_difference' % x for x in range(1,numBands+1)])

        for s in Shadowers:
            print(s)
            for w in Words:
                print(w)
                for b in Block.keys():
                    if b == 'Baseline':
                        continue
                    print(b)
                    shadowed_path = get_shadower_path(w,s,b)
                    model_path = get_model_path(w)
                    baseline_path = get_shadower_path(w,s,'Baseline')

                    if not os.path.isfile(shadowed_path):
                        continue

                    if not os.path.isfile(model_path):
                        continue

                    if not os.path.isfile(baseline_path):
                        continue
                    mod_env = calc_envelope(model_path,num_bands=numBands,erb=False)
                    base_env = calc_envelope(baseline_path,num_bands=numBands,erb=False)
                    shad_env = calc_envelope(shadowed_path,num_bands=numBands,erb=False)
                    b_to_m_sim,b_to_m_bandScores = envelope_match(mod_env,base_env,returnBandScores =True)
                    s_to_m_sim,s_to_m_bandScores = envelope_match(mod_env,shad_env,returnBandScores =True)
                    bands = [ s_to_m_bandScores[x] - b_to_m_bandScores[x] for x in range(numBands)]
                    csvw.writerow([os.path.split(baseline_path)[1], os.path.split(shadowed_path)[1], os.path.split(model_path)[1],
                                    b_to_m_sim,s_to_m_sim] + bands)
