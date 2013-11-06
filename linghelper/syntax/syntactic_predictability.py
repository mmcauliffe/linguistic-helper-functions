

#def getSynProbList():
    #f = open(fetch_media_resource("Gahl2004/gahl2004norms.txt")).read().splitlines()
    #lines = []
    #for i in xrange(1,len(f)):
        #line = f[i].split("\t")
        #if int(line[1]) > 0:
            #lines.append(line[0])
    #newlines = []
    #for line in lines:
        #newlines.extend(findAffixedForms(line))
    #return set(newlines)

#irreg = ['break','buy','choose','draw','drink',
         #'drive','eat','fight','find','fly','forget',
         #'freeze','grow','hang','hear','keep','know',
         #'leave','lose','pay','rise','say','see','shrink','sing','sit','slide',
         #'stand','strike','swear','sweep','swing','teach','tear','tell','think',
         #'understand','write']


#vowels = ['i','a','u','o','e']
#doubExcept = ['w','y','x']

#def addGerund(word):
    #affixed = []
    #if word[-1] not in vowels and word[-2] in vowels and word[-1] not in doubExcept:
        #affixed.append(word+word[-1]+'ing')
    #elif word[-1] == 'e' and word[-2] !='e':
        #affixed.append(word[:-1]+'ing')
    #else:
        #affixed.append(word+'ing')
    #return affixed

#def addIrreg(word):
    #affixed = []
    #if word == 'break':
        #affixed.extend(['broken','broke'])
    #elif word == 'buy':
        #affixed.extend(['bought'])
    #elif word == 'choose':
        #affixed.extend(['chose'])
    #elif word == 'draw':
        #affixed.extend(['drew','drawn'])
    #elif word == 'drink':
        #affixed.extend(['drank','drunk','dranken','drunken'])
    #elif word == 'drive':
        #affixed.extend(['drove','drive'])
    #elif word == 'eat':
        #affixed.extend(['ate','eaten'])
    #elif word == 'fight':
        #affixed.extend(['fought'])
    #elif word == 'find':
        #affixed.extend(['found'])
    #elif word == 'fly':
        #affixed.extend(['flew','flown'])
    #elif word == 'forget':
        #affixed.extend(['forgot','forgotten'])
    #elif word == 'freeze':
        #affixed.extend(['froze','frozen'])
    #elif word == 'grow':
        #affixed.extend(['grew','grown'])
    #elif word == 'hang':
        #affixed.extend(['hung'])
    #elif word == 'hear':
        #affixed.extend(['heard'])
    #elif word == 'keep':
        #affixed.extend(['kept'])
    #elif word == 'know':
        #affixed.extend(['knew','known'])
    #elif word == 'leave':
        #affixed.extend(['left'])
    #elif word == 'lose':
        #affixed.extend(['lost'])
    #elif word == 'pay':
        #affixed.extend(['paid'])
    #elif word == 'rise':
        #affixed.extend(['rose','risen'])
    #elif word == 'say':
        #affixed.extend(['said'])
    #elif word == 'see':
        #affixed.extend(['saw','seen'])
    #elif word == 'shrink':
        #affixed.extend(['shrunk','shrunken'])
    #elif word == 'sing':
        #affixed.extend(['sang','sung'])
    #elif word == 'slide':
        #affixed.extend(['slid','slidden'])
    #elif word == 'stand':
        #affixed.extend(['stood'])
    #elif word == 'strike':
        #affixed.extend(['struck'])
    #elif word == 'swear':
        #affixed.extend(['swore','sworn'])
    #elif word == 'sweep':
        #affixed.extend(['swept'])
    #elif word == 'swing':
        #affixed.extend(['swung'])
    #elif word == 'teach':
        #affixed.extend(['taught'])
    #elif word == 'tear':
        #affixed.extend(['tore','torn'])
    #elif word == 'tell':
        #affixed.extend(['told'])
    #elif word == 'think':
        #affixed.extend(['thought'])
    #elif word == 'understand':
        #affixed.extend(['understood'])
    #elif word == 'write':
        #affixed.extend(['wrote','written'])
    #return affixed

#def addPresent(word):
    #affixed = []
    #if word[-1] == 's' or word[-1] == 'z' or word[-1] == 'x' or word[-2:] == 'ch' or word[-2:] == 'sh':
        #affixed.append(word+"es")
    #elif word[-1] =='y' and word[-2] not in vowels:
        #affixed.append(word[:-1]+"ies")
    #else:
        #affixed.append(word+"s")
    #return affixed

#def addPast(word):
    #affixed = []
    #if word[-1] == 'e' and word[-2] not in vowels:
        #affixed.append(word+'d')
    #elif word[-1] not in vowels and word[-2] in vowels and word[-3] not in vowels and word[-1] not in doubExcept:
        #affixed.append(word+word[-1]+'ed')
    #elif word[-1] == 'y' and word[-2] not in vowels:
        #affixed.append(word[:-1]+'ied')
    #else:
        #affixed.append(word+"ed")
    #return affixed

#def findAffixedForms(word):
    #affixed = [word]
    #if word in irreg:
        #affixed.extend(addIrreg(word))
    #affixed.extend(addGerund(word))
    #affixed.extend(addPresent(word))
    #affixed.extend(addPast(word))
    #return affixed

#irreg_nouns = ['goose','foot','man','woman','mouse','tooth',
               #'deer','fish','sheep','species','child',
               #'ox','hero','potato','volcano','louse']

#def irregPlural(noun):
    #if noun == 'goose':
        #return [noun,'geese']
    #elif noun == 'foot':
        #return [noun,'feet']
    #elif noun == 'louse':
        #return [noun,'lice']
    #elif noun == 'man':
        #return [noun,'men']
    #elif noun == 'woman':
        #return [noun,'women']
    #elif noun == 'mouse':
        #return [noun,'mice']
    #elif noun == 'tooth':
        #return [noun,'teeth']
    #elif noun == 'deer':
        #return [noun]
    #elif noun == 'fish':
        #return [noun]
    #elif noun == 'sheep':
        #return [noun]
    #elif noun == 'species':
        #return [noun]
    #elif noun == 'child':
        #return [noun,'children']
    #elif noun == 'ox':
        #return [noun,'oxen']
    #elif noun == 'hero':
        #return [noun,'heroes']
    #elif noun == 'potato':
        #return [noun,'potatoes']
    #elif noun == 'volcano':
        #return [noun,'volcanoes','volcanos']

#def addPlural(noun):
    #if noun in irreg_nouns:
        #return irregPlural(noun)
    #if noun[-1] == 's' or noun[-1] == 'x' or noun[-1] == 'z':
        #plural = noun+'es'
    #elif noun[-1] == 'f':
        #plural = noun[:-1] + "ves"
    #elif len(noun) > 1 and noun[-2:] == 'ch' or noun[-2:] == 'sh':
        #plural = noun + "es"
    #elif len(noun) > 1 and noun[-2:] == 'fe':
        #plural = noun[:-2] + "ves"
    #elif len(noun) > 1 and noun[-1] == 'y' and not noun[-2] in vowels:
        #plural = noun[:-1] + "ies"
    #else:
        #plural = noun + 's'

    #return [noun,plural]
