import itertools
from linghelper.phonology.blick import BlickLoader,word_list

def guessStress(input_string):
    b = BlickLoader()
    vows = {x[:-1]: { y[-1] for y in b.vowels if y[:-1] == x[:-1]} for x in b.vowels}
    phones = input_string.split(" ")
    stress_pattern_space = [ vows[x] for x in phones if x in vows]
    revised_string = []
    for p in phones:
        if p in vows:
            revised_string.append(p+"%s")
        else:
            revised_string.append(p)
    revised_string = ' '.join(revised_string)
    possible_patterns = list(itertools.product(*stress_pattern_space))
    possible_strings = [revised_string % x for x in possible_patterns]
    best = 1000
    pattern = ''
    for p in possible_strings:
        if p in word_list:
            return p
        score = b.assessWord(p)
        if score < best:
            best = score
            pattern = p

    return pattern
