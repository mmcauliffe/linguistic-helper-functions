import os
import re
import random
from csv import DictReader,DictWriter

from linghelper.representations import Word

IPHOD_PATH = '/home/michael/dev/Corpora/IPHOD/IPhOD2_Words.txt'

DIALECT_MERGER = [('AA','AO')]

SETTINGS = {
            'NSylls':[2,3,4,5],
            'CVSkel': [''],
            'Critical segments': ['S','SH'],
            'Avoided segments': ['Z','ZH','CH','JH'],
            'Critical position in syllable':['coda'],
            'Critical syllable position in word': ['final','penultimate'],
            'Critical trials per segment': 10,
            'Filler trials': 140,
            'Return all': True,
            'No title case': True,
            'No plurals': True,
            'No gerunds': True,
            'No past tense': True,
            }

TRANS = set([])

VOWELS = set(['EY','IY','IH','AH','ER','AW','AY','OY','AA','AO','EH','UH','UW','OW','AE'])

def read_iphod():
    outlist = []
    with open(IPHOD_PATH,'r') as f:
        out = DictReader(f,delimiter='\t')
        for l in out:
            for k in l.keys():
                if k not in ['Word','UnTrn','StTrn','NSyll','NPhon','unsDENS','SFreq']:
                    del l[k]
            if 'CVC' in SETTINGS['CVSkel']:
                trans = l['UnTrn'].split('.')
                if len(trans) != 3:
                    continue
                if trans[0] not in VOWELS and trans[1] in VOWELS and trans[2] not in VOWELS:
                    outlist.append(l)
                    TRANS.update([l['UnTrn']])
            if int(l['NSyll']) in SETTINGS['NSylls']:
                outlist.append(l)
                TRANS.update([l['UnTrn']])
    return outlist

def output_list(to_save,path):
    head = to_save[0].keys()
    with open(path,'w') as f:
        csvwriter = DictWriter(f,head,delimiter='\t')
        csvwriter.writerow({x: x for x in head})
        for l in to_save:
            csvwriter.writerow(l)

def get_filler_words(iphod):
    fillers = []
    for w in iphod:
        w = Word(w['Word'],w['UnTrn'])
        if w.istitle():
            continue
        bad_segment = False
        for s in SETTINGS['Avoided segments'] + SETTINGS['Critical segments']:
            if w.contains(s):
                bad_segment = True
        if bad_segment:
            continue
        fillers.append({'Word':w.orthography,'Transcription':w.render_transcription()})
    return fillers

def get_target_words(iphod,sound,sylpos,wordpos):
    targets = []
    for w in iphod:
        w = Word(w['Word'],w['UnTrn'])
        if w.istitle():
            continue
        if not w.in_position(sound,sylpos,wordpos):
            continue
        bad_segment = False
        for s in SETTINGS['Avoided segments']:
            if w.contains(s):
                bad_segment = True
        other_critical_segs = filter(lambda x: x != sound, SETTINGS['Critical segments']) + SETTINGS['Avoided segments']
        for oc in other_critical_segs:
            if w.neighbour_transcription(oc,sylpos,wordpos) in TRANS:
                bad_segment = True
                break
            if w.segment_count(oc) > 0:
                bad_segment = True
                break
        if bad_segment:
            continue
        if w.segment_count(sound) > 1:
            continue
        targets.append({'Word':w.orthography,'Transcription':w.render_transcription()})
    return targets

#def get_target_words(iphod, sound, position):
    ##relevant_neighbours = filter(lambda x: x != sound, ['S','SH','Z','ZH','F','V','TH','DH'])
    #all_sounds = ['S','SH','Z','ZH']
    #relevant_neighbours = filter(lambda x: x != sound, all_sounds)
    #targets = []
    #for i in iphod:
        #trans = i['UnTrn'].split('.')
        #if trans[position] != sound:
            #continue
        #if i['Word'].istitle():
            #continue
        #if trans[-1] in ['S','Z']:
            #if '.'.join(trans[:-1]) in TRANS:
                #continue
        #good = False
        #if position < 0:
            #temp_pos = len(trans) + position
        #else:
            #temp_pos = position
        #for t in range(len(trans)):
            #if t == temp_pos:
                #for s in relevant_neighbours:
                    #trans[t] = s
                    #if '.'.join(trans) in TRANS:
                        #break
                #else:
                    #good = True
                #trans[t] = sound
                #if not good:
                    #break
            #elif trans[t] in all_sounds:
                #break
        #else:
            #targets.append(i)
    #return targets

if __name__ == '__main__':
    iphod = read_iphod()
    filler_list = get_filler_words(iphod)
    random.shuffle(filler_list)
    output_list(filler_list,'/home/michael/Documents/Linguistics/Projects/Perceptual Learning/Pilot/Lists/fillers.txt')
    for sound in SETTINGS['Critical segments']:
        for sylpos in SETTINGS['Critical position in syllable']:
            for wordpos in SETTINGS['Critical syllable position in word']:
                target_list = get_target_words(iphod,sound,sylpos,wordpos)
                random.shuffle(target_list)
                print ', '.join([x['Word'] for x in target_list][:10])
                output_list(target_list,'/home/michael/Documents/Linguistics/Projects/Perceptual Learning/Pilot/Lists/%s_%s_%s.txt'%(sound,sylpos,wordpos))
