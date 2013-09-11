import subprocess
import math
import re
import os
import pickle
from collections import Counter

#WordNet imports
import nltk
from nltk.corpus.reader import wordnet

#N-gram generation through scikit-learn package
from sklearn.feature_extraction.text import CountVectorizer

#Stop word list from WordNet::Similarity module for Perl (Pedersen et al 2004)
from media.stoplist import stop_list

def convert_IDF_to_prob(IDF):
    return math.pow(math.e,IDF*-1)

#Path to modified WordNet::Similarity script (only uses Extended Lesk measure)
SEM_PRED = os.path.join(os.path.dirname(os.path.abspath(__file__)),'media','SemPred.pl')



class SemanticPredictabilityAnalyzer:
    """
    Class for analyzing semantic predictability.

    Methods for analysis include bag of words overlaps and bag of n-grams
    overlaps from WordNet senses.  Defaults to bag of words without IDF
    scoring.

    Also has methods for disambiguating senses in WordNet.
    """
    def __init__(self,ngram=False,use_idf=False):
        self.ngram = ngram
        self.use_idf = use_idf

        #Load WordNet synsets and download data if necessary
        try:
            wordnet_path = nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
            wordnet_path = nltk.data.find('corpora/wordnet')
        self.wn = wordnet.WordNetCorpusReader(wordnet_path)

        #Initialize the two types of n-gram generators
        pentagram_vectorizer = CountVectorizer(ngram_range=(1, 5),
                                     token_pattern=r'\b[A-Za-z]+\b', min_df=1,stop_words=stop_list)
        unigram_vectorizer = CountVectorizer(ngram_range=(1, 1),
                                     token_pattern=r'\b[A-Za-z]+\b', min_df=1,stop_words=stop_list)

        #Function for generating five-grams through unigrams
        self.pent_analyze = pentagram_vectorizer.build_analyzer()

        #Function for generating just unigrams
        self.uni_analyze = unigram_vectorizer.build_analyzer()

        #Load IDF scores
        self.IDF = self.get_idf_scores()
        self.counts = self.get_counts()

    def reduce_sense(self,sense):
        """
        Reduce a sense's gloss and examples into a bag of words/ngrams.
        """
        if self.ngram:
            bag = set(self.pent_analyze(sense.definition))
            for e in sense.examples:
                bag.update(self.pent_analyze(e))
        else:
            bag = set(self.uni_analyze(sense.definition))
            for e in sense.examples:
                bag.update(self.uni_analyze(e))
        return bag

    def get_counts(self):
        counts = Counter()
        for s in self.wn.all_synsets():
            counts.update(s.definition.split(' '))
            for e in s.examples:
                counts.update(e.split(' '))
        return counts

    def get_idf_scores(self):
        """
        Calculate inverse document frequency for every word used in
        WordNet.
        """
        scores = Counter()
        for s in self.wn.all_synsets():
            scores.update(self.reduce_sense(s))
        tot_count = float(len(list(wn.all_synsets())))
        for k in scores:
            scores[k] = -1 * math.log(float(scores[k])/tot_count)
        return scores



    def generate_bag(self,sense):
        """
        Function to generate a bag of words/ngrams from a given sense
        and every sense related to it by any type of relation in WordNet.
        """
        bag = self.reduce_sense(sense)
        for l in [sense.hypernyms(),sense.hyponyms(),
                    sense.member_holonyms(),sense.substance_holonyms(),
                    sense.part_holonyms(),sense.member_meronyms(),
                    sense.substance_meronyms(),sense.part_meronyms(),
                    sense.topic_domains(),sense.region_domains(),
                    sense.usage_domains(),sense.attributes(),
                    sense.entailments(),sense.causes(),
                    sense.also_sees(),sense.verb_groups(),
                    sense.similar_tos()]:
            for s in l:
                bag.update(self.reduce_sense(s))
        return bag

    def relatedness(self,sense_one,sense_two):
        """
        Assess the semantic relatedness of two senses by overlaps in
        their bag of words/ngrams.
        """
        bag_one = self.generate_bag(sense_one)
        bag_two = self.generate_bag(sense_two)
        inter = bag_one & bag_two
        if self.ngram:
            score = 0.0
            #Eliminate overlaps that are subsumed by longer length ngrams
            for i in inter:
                for j in inter:
                    if i != j and re.search(r'\b'+i+r'\b',j) is not None:
                        break
                else:
                    if self.use_idf:
                        #If we're using IDF scoring, sum the scores and square
                        s = float(sum([self.IDF[x] for x in i.split(' ')]))
                        score += s * s
                    else:
                        #Otherwise, n overlap scores n^2
                        score += float(len(i.split(' '))) * float(len(i.split(' ')))
            return score
        else:
            if self.use_idf:
                return sum([self.IDF[i] for i in inter])
            return len(inter)

    def get_word_context_relatedness(self,word_sense,context_senses,style='average'):
        """
        Given a word sense and a list of context senses, return a
        semantic predictability score.
        """
        if isinstance(word_sense,str):
            #Convert to WordNet sense if we get a string 'word.c.1'
            word_sense = self.to_wordnet_sense(word_sense)

        #Abort if no word sense is found
        if word_sense is None:
            return 'NA'
        score = 0.0
        for s in context_senses:
            if isinstance(s,str):
                s = self.to_wordnet_sense(s)

            #Skip over context senses that aren't found
            if s is None:
                continue
            score += self.relatedness(word_sense,s)

        #If the style is average try to normalize the score by the number
        #of context words, but don't if there aren't any context words,
        #in which case return 0.0
        if style == 'average':
            try:
                score = float(score)/float(len(context_senses))
            except ZeroDivisionError:
                pass
        return score

    def to_wordnet_sense(self,sense_string):
        """
        Attempt to convert a string of the form WORD.CAT.# like 'cat.n.1'
        into a WordNet sense.

        Returns None if no sense is found.
        """
        try:
            return self.wn.synset(sense_string)
        except wordnet.WordNetError:
            return None

    def get_semantic_predictability(self,word,cat,prev_context,foll_context):
        #P(Word | Context) = P(Context | Word) * P(Word) / P(Context)

        #P(Context | Word) ~= P(Context | Synset_disambiguated)

        sense = self.disambiguate_sense(word,cat,prev_context,foll_context)


    def disambiguate_sense(self,word,cat,prev_context,foll_context,to_string=False):
        """
        Given a word, its category, and its surrounding context, find the
        word sense that best matches the surround context, using Simple
        Lesk algorithm.

        Returns either a Synset instance or a string corresponding to that
        Synset instance, and returns None if the word-category combo is
        not found in WordNet.
        """

        synsets = self.wn.synsets(word,pos=cat)
        if len(synsets) == 0:
            return None

        #Grab three content words on each side of the given word
        prev_words = self.uni_analyze(prev_context)[-3:]
        foll_words = self.uni_analyze(foll_context)[:3]
        context = prev_words + foll_words

        #Default to the most common sense in WordNet
        best_sense = synsets[0]
        best_score = 0
        for s in synsets:
            #For each possible sense
            #Get a bag of words from the gloss and examples
            words = set(self.uni_analyze(s.definition))
            for e in s.examples:
                words.update(self.uni_analyze(e))

            #Assign it a score equal to the IDF of overlapping words
            #between the context and the sense
            score = sum([ self.IDF[x] for x in context if x in words])

            #Save if the score is better than the current best score
            if score > best_score:
                best_sense = s

        if to_string:
            return best_sense.name
        return best_sense

def perl_get_semantic_predictability(word,context,debug=False,style='average'):
    """
    Compute Extended Lesk measure from WordNet::Similarity between a given
    word and each word in the context.
    """

    #Create call to the perl script media/SemPred.pl
    com = ["perl",SEM_PRED,word,','.join(context)]
    p = subprocess.Popen(com,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    stdout, stderr = p.communicate()

    if debug:
        print(stdout)
        print(stderr)

    #If there was no context, return 0.0
    if stdout == '':
        return 0.0

    #Otherwise return the sum or the average of the scores depending on the style
    scores = stdout.split(",")
    sempred = sum(map(float,scores))

    if style == 'average':
        try:
            return sempred / float(len(scores))
        except ZeroDivisionError:
            return 0.0

    return sempred

def evaluate_sentences():
    """
    Evaluate sentences that have been assigned high or low predictability.

    Test files have been annotated manually with context words tagged
    for part of speech.  All words use the default sense in WordNet.
    """

    #Create an instance of the four types of analyzer
    unigram_noidf_analyzer = SemanticPredictabilityAnalyzer()
    unigram_idf_analyzer = SemanticPredictabilityAnalyzer(use_idf=True)
    ngram_noidf_analyzer = SemanticPredictabilityAnalyzer(ngram=True)
    ngram_idf_analyzer = SemanticPredictabilityAnalyzer(ngram=True,use_idf=True)
    test_dir = '/home/michael/devR/503Project'
    head_scar = None
    sentences = []

    #Load file containing sentences from Scarborough (2010) study
    with open(os.path.join(test_dir,'scarborough.txt'),'r') as f:
        for line in f:
            l = line.strip().split('\t')
            if len(l) == 1:
                continue
            if head_scar is None:
                head_scar = l
                continue
            newline = {head_scar[i]:l[i] for i in range(len(l))}
            sentences.append(newline)

    #Load file containing sentences from Kalikow et al. (1977) study
    head = None
    with open(os.path.join(test_dir,'kalikow.txt'),'r') as f:
        for line in f:
            l = line.strip().split('\t')
            if len(l) == 1:
                continue
            if head is None:
                head = l
                continue
            newline = {head[i]:l[i] for i in range(len(l)) if head[i] in head_scar}
            sentences.append(newline)

    #Output the results of the semantic predictability analyzer with the
    #various settings available
    with open(os.path.join(test_dir,'measures.txt'),'w') as f:
        head = head_scar + ['perl_sim','bag_words_noidf','bag_ngrams_noidf','bag_words_idf','bag_ngrams_idf']
        f.write('\t'.join(head))
        for s in sentences:
            f.write('\n')

            #WordNet::Similarity module uses # as breaks in senses
            #instead of . in WordNet
            perl_context = map(lambda x: x+'#1',s['Context'].split(','))
            perl_word = s['Final word'] + '#n#1'
            wordnet_context = map(lambda x: x.replace('#','.'),perl_context)
            wordnet_word = perl_word.replace('#','.')

            s['perl_sim'] = perl_get_semantic_predictability(perl_word,perl_context)
            s['bag_words_noidf'] = unigram_noidf_analyzer.get_semantic_predictability(
                                        wordnet_word,
                                        wordnet_context)
            s['bag_ngrams_noidf'] = ngram_noidf_analyzer.get_semantic_predictability(
                                        wordnet_word,
                                        wordnet_context)
            s['bag_words_idf'] = unigram_idf_analyzer.get_semantic_predictability(
                                        wordnet_word,
                                        wordnet_context)
            s['bag_ngrams_idf'] = ngram_idf_analyzer.get_semantic_predictability(
                                        wordnet_word,
                                        wordnet_context)
            f.write('\t'.join([str(s[x]) for x in head]))


if __name__ == '__main__':
    #Run the test evaluation of the sentences
    #evaluate_sentences()
    p = SemanticPredictabilityAnalyzer()

