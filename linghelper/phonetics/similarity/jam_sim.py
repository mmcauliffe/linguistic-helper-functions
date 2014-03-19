import os
import subprocess
import sys
import csv

sys.path.append('/home/michael/dev/Linguistics/linguistic-helper-functions')
sys.path.append('/home/michael/dev/Linguistics/python-praat-scripts')
from linghelper.phonetics.similarity.envelope import envelope_similarity,calc_envelope,envelope_match
from linghelper.phonetics.similarity.spectral import mfcc_distance,spectral_distance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JAM_DIR = os.path.normpath('/home/michael/dev/Data/Jam')
MODEL_DIR = os.path.join(JAM_DIR,'modeltalker')

Speakers = os.listdir(JAM_DIR)

Words = ['bag', 'bead', 'beet', 'beg', 'bet', 'blues',
            'boat', 'boost', 'boot', 'breed', 'cask',
            'chap', 'chat', 'cheap', 'cheat', 'check',
            'chief', 'choke', 'chute', 'cloak', 'clog',
            'clop', 'clue', 'cod', 'code', 'crab', 'crack',
            'dead', 'debt', 'deep', 'deuce', 'dock', 'dope',
            'dot', 'douche', 'doze', 'drag', 'dude', 'duke',
            'fat', 'feed', 'flag', 'flap', 'flash', 'flat',
            'flock', 'flute', 'gag', 'gnat', 'goat', 'heap',
            'heed', 'hoop', 'hoot', 'hope', 'jet', 'knock',
            'lab', 'lack', 'lag', 'let', 'loop', 'loot',
            'mass', 'mat', 'mosque', 'nag', 'net', 'peak',
            'peck', 'peg', 'pep', 'pest', 'pet', 'plod',
            'plot', 'poach', 'poke', 'pope', 'quote',
            'rack', 'rag', 'road', 'rob', 'rock', 'sack',
            'sag', 'scope', 'seek', 'set', 'shock', 'slot',
            'smock', 'soak', 'sock', 'sod', 'soup', 'sped',
            'stack', 'stag', 'stead', 'step', 'stoke', 'stoop',
            'stop', 'suit', 'tad', 'tag', 'teak', 'tease',
            'teeth', 'thieve', 'those', 'tooth', 'tote', 'treat',
            'trod', 'tube', 'tuque', 'vast', 'vet', 'weak', 'wed',
            'weed', 'weep', 'wove', 'wreck', 'wrote', 'yacht', 'yak']

Productions = ['1','2']

opt_dict = {
            'num_bands':8,
            'erb':False
            }

def do_post_and_base():

    output = []

    for w in Words:
        mod_path = os.path.join(MODEL_DIR,'modeltalker_%s.wav' %w)
        mod_env = calc_envelope(mod_path,**opt_dict)
        print(w)
        for s in Speakers:
            if 'IS' in s:
                continue
            if s == 'modeltalker':
                continue
            sp = s.split('_')[0]
            s_dir = os.path.join(JAM_DIR,s)
            base_path = os.path.join(s_dir,'%s_%s1.wav' % (sp,w))
            shad_path = os.path.join(s_dir,'%s_%s2.wav' % (sp,w))
            if not os.path.isfile(base_path):
                continue
            if not os.path.isfile(shad_path):
                continue
            base_env = calc_envelope(base_path,**opt_dict)
            shad_env = calc_envelope(shad_path,**opt_dict)
            b_to_m_sim = envelope_match(mod_env,base_env)
            s_to_m_sim = envelope_match(mod_env,shad_env)
            output.append([sp,w,b_to_m_sim,s_to_m_sim])


    with open(os.path.join(BASE_DIR,'jam_output8IS.txt'),'w') as f:
        csvw = csv.writer(f,delimiter='\t')
        csvw.writerow(['Shadower_number',
                        'Word','shad_to_mod_env_sim','base_to_mod_env_sim',
                        #'mfcc_shad_to_mod','mfcc_mod_to_shad',
                        #'spec_shad_to_mod','spec_mod_to_shad',
                        #'mfcc_base_to_mod','mfcc_mod_to_base',
                        #'spec_base_to_mod','spec_mod_to_base'
                        ])
        for l in output:
            csvw.writerow(l)

def do_IS_speakers():
    output = []
    Productions = ['2','3']
    for w in Words:
        mod_path = os.path.join(MODEL_DIR,'modeltalker_%s.wav' %w)
        mod_env = calc_envelope(mod_path,**opt_dict)
        print(w)
        for s in Speakers:
            if 'IS' not in s:
                continue
            if s == 'modeltalker':
                continue
            sp = s.split('_')[0]
            s_dir = os.path.join(JAM_DIR,s)
            for p in Productions:
                base_path = os.path.join(s_dir,'%s_%s1is.wav' % (sp,w))
                shad_path = os.path.join(s_dir,'%s_%s%sis.wav' % (sp,w,p))
                if not os.path.isfile(base_path):
                    continue
                if not os.path.isfile(shad_path):
                    continue
                base_env = calc_envelope(base_path,**opt_dict)
                shad_env = calc_envelope(shad_path,**opt_dict)
                b_to_m_sim = envelope_match(mod_env,base_env)
                s_to_m_sim = envelope_match(mod_env,shad_env)
                output.append([sp,p,w,b_to_m_sim,s_to_m_sim])


    with open(os.path.join(BASE_DIR,'jam_output8IS.txt'),'w') as f:
        csvw = csv.writer(f,delimiter='\t')
        csvw.writerow(['Shadower_number','Block',
                        'Word','base_to_mod_env_sim','shad_to_mod_env_sim',
                        #'mfcc_shad_to_mod','mfcc_mod_to_shad',
                        #'spec_shad_to_mod','spec_mod_to_shad',
                        #'mfcc_base_to_mod','mfcc_mod_to_base',
                        #'spec_base_to_mod','spec_mod_to_base'
                        ])
        for l in output:
            csvw.writerow(l)

if __name__ == '__main__':
    do_IS_speakers()

