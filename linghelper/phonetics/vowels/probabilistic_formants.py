from numpy import exp

from linghelper.phonetics.representations.amplitude_envelopes import to_gammatone_envelopes

def sigmoid(x,alpha,theta):
    y = 1/(1+exp(-1*alpha*(x-theta)))
    return y

def auditory_representation(path,gammatone=False):
    num_bands = 128
    freq_lims = (80,8000)
    
    