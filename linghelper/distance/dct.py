
from scipy.fftpack import dct
from scipy.spatial.distance import euclidean

def dct_distance(source,target,norm=True,numC=3):
    numBands = source.shape[1]
    distVal = 0
    for i in range(numBands):
        source_dct = dct(source[:,i],norm='ortho')
        if norm:
            source_dct = source_dct[1:]
        source_dct = source_dct[0:numC]
        target_dct = dct(target[:,i],norm='ortho')
        if norm:
            target_dct = target_dct[1:]
        target_dct = target_dct[0:numC]
        distVal += euclidean(source_dct,target_dct)
    return distVal/numBands
        
