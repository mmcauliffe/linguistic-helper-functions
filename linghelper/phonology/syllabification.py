import re

from constants import ENGLISH_ONSETS  as ONSETS,ENGLISH_VOWEL_PATTERN as VOWEL_PATTERN

class Word(object):
    def __init__(self,orthography,transcription):
        self.orthography = orthography
        self.syllables = syllabify(transcription)

    def contains(self,sound):
        for s in self.syllables:
            return s.contains(sound)
        return False

    def in_position(self,sound,syllable_position,word_position, complex=False):
        if word_position == 'initial':
            s = self.syllables[0]
        elif word_position == 'final':
            s = self.syllables[-1]
        if syllable_position == 'onset':
            if complex:
                return s.in_onset(sound)
            else:
                return s.onset_is(sound)
        elif syllable_position == 'coda':
            if complex:
                return s.in_coda(sound)
            else:
                return s.coda_is(sound)
        else:
            return s.nucleus_is(sound)
        return False

    def render_transcription(self,flat=True):
        if flat:
            sep = self.syllables[0].sep
            return sep.join(map(str,self.syllables))

    def __str__(self):
        return '%s, %s' % (self.orthography,self.render_transcription())


class Syllable(object):
    def __init__(self,nucleus, onset=[],coda=[],sep='.'):
        self.nucleus = nucleus
        self.onset = onset
        self.coda = coda
        self.sep = sep

    def in_onset(self,sound):
        if sound in self.onset:
            return True
        return False

    def onset_is(self,sound):
        if self.onset_string() == sound:
            return True
        return False

    def in_coda(self,sound):
        if sound in self.coda:
            return True
        return False

    def coda_is(self,sound):
        if self.coda_string() == sound:
            return True
        return False

    def nucleus_is(self,sound):
        if sound == self.nucleus:
            return True
        return False

    def contains(self,sound):
        if re.match(VOWEL_PATTERN,sound):
            return self.nucleus_is(sound)
        else:
            if self.in_onset(sound):
                return True
            if self.in_coda(sound):
                return True
        return False

    def onset_string(self):
        return self.sep.join(self.onset)

    def coda_string(self):
        return self.sep.join(self.coda)

    def __str__(self):
        return self.sep.join([x for x in [self.onset_string(),self.nucleus,self.coda_string()] if x])

def syllabify(inputword):
    #verify if list
    sep = '.'
    if isinstance(inputword,str):
        if ' ' in inputword:
            sep = ' '
        inputword = inputword.split(sep)
    cons = []
    syllables = []
    while inputword:
        cur = inputword.pop(0)
        if re.match(VOWEL_PATTERN,cur):
            s = Syllable(nucleus = cur,sep=sep)
            if syllables:
                for i in range(len(cons)):
                    if ' '.join(cons[i:]) in ONSETS:
                        s.onset = cons[i:]
                        syllables[-1].coda = cons[:i]
                        break
            else:
                s.onset = cons
            cons = []
            syllables.append(s)
        else:
            cons.append(cur)
    if cons:
        syllables[-1].coda = cons
    return syllables

if __name__ == '__main__':
    tests = [['','B.AE.D'],
                ['','B.AE.S.D.IY'],
                ['','AH.B.AE.S.T.IY'],
                ['','AH0.B.AE0.D.IY1']]
    for t in tests:
        w = Word(*t)
        print map(str,w.syllables)
        print w.in_position('T','onset','final')


