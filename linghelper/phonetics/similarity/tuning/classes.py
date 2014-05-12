import os
import random
from csv import DictReader
from collections import Counter
from functools import partial
from math import log

from scipy.stats.stats import pearsonr

from linghelper.phonetics.representations.amplitude_envelopes import to_envelopes
from linghelper.phonetics.representations.mfcc import to_mfcc, to_melbank, to_mfcc_praat
from linghelper.phonetics.representations.prosody import to_pitch, to_intensity
from linghelper.distance.dtw import dtw_distance
from linghelper.distance.xcorr import xcorr_distance
from linghelper.distance.dct import dct_distance


class DataSet(object):
    def __init__(self,directory,lookup_functions,words,productions = None,additional_model_info = None):
        self.lookups = lookup_functions
        self.model_dir = os.path.join(directory,'Models')
        self.shadower_dir = os.path.join(directory,'Shadowers')
        subdirs = os.listdir(self.model_dir)
        if 'Female' in subdirs:
            self.use_gender = True
            male_models = os.listdir(os.path.join(self.model_dir,'Male'))
            female_models = os.listdir(os.path.join(self.model_dir,'Female'))
            self.models = list(map(lambda x: [x,'Male'],male_models))
            self.models += list(map(lambda x: [x,'Female'],female_models))
            male_shadowers = os.listdir(os.path.join(self.shadower_dir,'Male'))
            female_shadowers = os.listdir(os.path.join(self.shadower_dir,'Female'))
            self.shadowers = list(map(lambda x: [x,'Male'],male_shadowers))
            self.shadowers += list(map(lambda x: [x,'Female'],female_shadowers))
        else:
            self.use_gender = False
            self.models = subdirs
            self.shadowers = os.listdir(self.shadower_dir)
        if productions is None:
            self.productions = ['Shadow']
        else:
            self.productions = productions
        if additional_model_info is not None:
            for i in range(len(self.models)):
                self.models[i] += additional_model_info[self.models[i][0]]
        self.words = words
        axb_files = [x for x in os.listdir(directory) if x.endswith('.txt')]
        self.mapping = self.generate_mapping()
        sum_dict = {}
        count_dict = {}
        for f in axb_files:
            with open(os.path.join(directory,f),'r') as csvfile:
                reader = DictReader(csvfile, delimiter = '\t')
                for line in reader:
                    tup = (line['Baseline'],line['Model'],line['Shadowed'])
                    if tup not in sum_dict:
                        sum_dict[tup] = 0
                    if tup not in count_dict:
                        count_dict[tup] = 0
                    sum_dict[tup] += int(line['ShadowResp'])
                    count_dict[tup] += 1
        self.listenerResp = {x: sum_dict[x]/count_dict[x] for x in sum_dict.keys()}
        
    def generate_mapping(self):
        path_mapping = []
        for w in self.words:
            for m in self.models:
                model_path = self.lookups['Model'](self.model_dir,m,w)
                if not os.path.exists(model_path):
                    continue
                for s in self.shadowers:
                    base_path = self.lookups['Baseline'](self.shadower_dir,s,w)
                    if not os.path.exists(base_path):
                        continue
                    for p in self.productions:
                        shad_path = self.lookups['Shadowed'](self.shadower_dir,m,s,w,p)
                        if not os.path.exists(shad_path):
                            continue
                        path_mapping.append((base_path,model_path,shad_path))
        return path_mapping
        
    def analyze_config(self,config):
        cache = {}
        num_bands=config.num_bands.get_value()
        freq_lims = (config.min_freq.get_value(),config.max_freq.get_value())
        window_length = config.window_length.get_value()
        time_step = config.time_step.get_value()
        use_praat = config.use_praat.get_value()
        num_coeffs = config.num_coeffs.get_value()
        num_bands = config.num_bands.get_value()
        if config.representation == 'envelopes':
            to_rep = partial(to_envelopes,num_bands=num_bands,freq_lims=freq_lims,gammatone=False)
        elif config.representation == 'mfcc':
            use_power = config.use_power.get_value()
            if use_praat:
                to_rep = partial(to_mfcc_praat, freq_lims=freq_lims, 
                                                numCC=num_coeffs,
                                                win_len=window_length,
                                                time_step=time_step)
            else:
                to_rep = partial(to_mfcc,freq_lims=freq_lims,
                                            numCC=num_coeffs,
                                            win_len=window_length,
                                            time_step=time_step,
                                            num_filters = num_bands, 
                                            use_power = use_power)
        elif config.representation == 'mhec':
            pass
        elif config.representation == 'gammatone':
            pass
        elif config.representation == 'melbank':
            to_rep = partial(to_melbank,freq_lims=freq_lims,
                                        win_len=window_length,
                                        time_step=time_step,
                                        num_filters = num_bands)
        elif config.representation == 'prosody':
            to_rep = partial(to_prosody,time_step=time_step)
            
        if config.match_algorithm == 'xcorr':
            dist_func = xcorr_distance
        elif config.match_algorithm == 'dtw':
            dist_func = dtw_distance
        elif config.match_algorithm == 'dct':
            dist_func = dct_distance
            
        x = []
        y = []
        for pm in self.mapping:
            listenertup = tuple(map(lambda x: os.path.split(x)[1],pm))
            if listenertup not in self.listenerResp:
                continue
            if pm[0] not in cache:
                cache[pm[0]] = to_rep(pm[0])
            if pm[1] not in cache:
                cache[pm[1]] = to_rep(pm[1])
            if pm[2] not in cache:
                cache[pm[2]] = to_rep(pm[2])
            base = cache[pm[0]]
            model = cache[pm[1]]
            shadow = cache[pm[2]]
            dist1 = dist_func(base,model)
            dist2 = dist_func(shadow,model)
            ratio = dist2 / dist1
            x.append(self.listenerResp[listenertup])
            y.append(ratio)
        correlation = pearsonr(x,y)
        return correlation[0]

class Param(object):
    def __init__(self,min_value,max_value,step):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.reset_value()
        
    def reset_value(self):
        if isinstance(self.max_value,float):
            self.value = random.randint(0, int((self.max_value - self.min_value) / self.step)) * self.step + self.min_value
        elif isinstance(self.max_value,bool):
            self.value = bool(random.randint(0,1))
        else:
            self.value = random.randrange(self.min_value,self.max_value,self.step)
        
    def get_value(self):
        return self.value

class Configuration(object):
    max_freq = Param(4000,10000,100)
    min_freq = Param(50,500,50)
    window_length = Param(0.005,0.05,0.005)
    time_step = Param(0.001,0.01,0.001)
    use_praat = Param(True,False,1)
    num_coeffs = Param(10,30,2)
    use_power = Param(False,True,1)
    num_bands = Param(4,48,2)
    
    def __init__(self,representation,match_algorithm):
        self.representation = representation
        self.match_algorithm = match_algorithm
        self.max_freq.reset_value()
        self.min_freq.reset_value()
        self.window_length.reset_value()
        self.time_step.reset_value()
        self.use_praat.value = False
        self.num_coeffs.reset_value()
        self.use_power.reset_value()
        self.num_bands.reset_value()
        
    def verify(self):
        if self.representation in ['mfcc','mhec']:
            while self.num_coeffs.get_value() > self.num_bands.get_value():
                self.num_coeffs.reset_value()
                self.num_bands.reset_value()
                
    def __str__(self):
        
        return '''
        Representation: %s
        Matching algorithm: %s
        Min freq: %d
        Max freq: %d
        Win len: %f
        Time step: %f
        Num coeffs: %d
        Num bands: %d
        Use power: %r
        Use Praat: %r
        ''' % (self.representation,self.match_algorithm,self.min_freq.get_value(),
                self.max_freq.get_value(),self.window_length.get_value(),self.time_step.get_value(),
                self.num_coeffs.get_value(), self.num_bands.get_value(), self.use_power.get_value(),
                self.use_praat.get_value())


class MfccConfig(Configuration):
    pass
    
class EnvelopeConfig(Configuration):
    pass
    
class MhecConfig(Configuration):
    pass
    
class GammatoneConfig(Configuration):
    pass
    
class MelBankConfig(Configuration):
    pass
    
    
