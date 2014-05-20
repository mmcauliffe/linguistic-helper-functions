from numpy import zeros,inf
from scipy.spatial.distance import euclidean
import operator

def dtw_distance(source,target):
    distMat = generate_distance_matrix(source,target)
    return regularDTW(distMat)

def generate_distance_matrix(source,target):
    #print(source.shape)
    #print(target.shape)
    assert(source.shape[1] == target.shape[1])
    sLen = source.shape[0]
    tLen = target.shape[0]
    distMat = zeros((sLen,tLen))
    for i in range(sLen):
        for j in range(tLen):
            distMat[i,j] = euclidean(source[i,:],target[j,:])
    return distMat

def regularDTW(distMat,distOnly=True):
    sLen,tLen = distMat.shape
    totalDistance = zeros((sLen+1,tLen+1))
    totalDistance[0,:] = inf
    totalDistance[:,0] = inf
    totalDistance[0,0] = 0
    totalDistance[1:sLen+1,1:tLen+1] = distMat
    
    minDirection = zeros((sLen+1,tLen+1))
    
    for i in range(sLen):
        for j in range(tLen):
            direction,minPrevDistance = min(enumerate([totalDistance[i,j],totalDistance[i,j+1],totalDistance[i+1,j]]), key=operator.itemgetter(1))
            totalDistance[i+1,j+1] = totalDistance[i+1,j+1] + minPrevDistance
            minDirection[i,j] = direction
    
    if distOnly:
        return totalDistance[sLen,tLen]
    
    mapping = zeros((max([sLen,tLen])*2,2))
    mapping[len(mapping),1] = sLen
    mapping[len(mapping),2] = tLen
    
    numSteps = 0
    i = sLen
    j = tLen
    while sLen > 0 or tLen > 0:
        numSteps += 1
        
        aDirection = minDirect[i,j]
        if aDirection == 1:
            i -= 1
            j -= 1
        elif aDirection == 2:
            i-= 1
        elif aDirection == 3:
            j -= 1
            
        if i < 0:
            i = 0
        if j < 0:
            j = 0
        
        mapping[len(mapping)-numSteps,1] = i
        mapping[len(mapping)-numSteps,2] = j
    mapping = mapping[len(mapping)-numSteps:len(mapping),:]
    return mapping
