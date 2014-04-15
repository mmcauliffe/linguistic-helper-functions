import numpy as np
from scipy.spatial.distance import euclidean
import operator

#from .media.constants import costs

#def  minEditDist(target, source,distOnly=False):
    #''' Computes the min edit distance from target to source. Figure 3.25 '''
    #def insertCost(seg):
        #return 1

    #def deleteCost(seg):
        #return 1

    #def substCost(segone,segtwo):
        #if segone == segtwo:
            #return 0
        #segone = segone.lower()
        #segtwo = segtwo.lower()
        #if (segone,segtwo) in costs:
            #return costs[(segone,segtwo)]
        #if (segtwo,segone) in costs:
            #return costs[(segtwo,segone)]
        #return 2

    #target = list(target)
    #source = list(source)

    #n = len(target)
    #m = len(source)

    #distance = [[0 for i in range(m+1)] for j in range(n+1)]
    #pointers = [[(0,0) for i in range(m+1)] for j in range(n+1)]

    #for i in range(1,n+1):
        #distance[i][0] = distance[i-1][0] + insertCost(target[i-1])
        #pointers[i][0] = (i-1,0)

    #for j in range(1,m+1):
        #distance[0][j] = distance[0][j-1] + deleteCost(source[j-1])
        #pointers[0][j] = (0,j-1)

    #for i in range(1,n+1):
        #for j in range(1,m+1):
            #dists = [distance[i-1][j]+1,
                                #distance[i][j-1]+1,
                                #distance[i-1][j-1]+substCost(source[j-1],target[i-1])]
            #ind = np.argmin(dists)
            #distance[i][j] = dists[ind]
            #if ind == 0:
                #pointers[i][j] = (i-1,j)
            #elif ind == 1:
                #pointers[i][j] = (i,j-1)
            #else:
                #pointers[i][j] = (i-1,j-1)
    #if distOnly:
        #return distance[n][m]
    ##alignment
    #i = n
    #j = m
    #mapping = []
    #finished = False
    #while not finished:
        #if i == 0 and j == 0:
            #finished = True
        #newi,newj = pointers[i][j]
        #if newi != i and newj != j:
            #mapping.append([target[i-1],source[j-1]])
        #elif newi != i:
            #mapping.append([target[i-1],'.'])
        #elif newj != j:
            #mapping.append(['.',source[j-1]])
        #i,j = newi,newj
    #mapping.reverse()
    #return distance[n][m],mapping

    #while i > -1 and j > -1:
        #candidates = []
        #print(mapping)
        #print(i,j)
        #if i > 0 and j > 0:
            #candidates.append(distance[i-1][j-1])
        #if i > 0:
            #candidates.append(distance[i-1][j])
        #if j > 0:
            #candidates.append(distance[i][j-1])
        #prevScore = min(candidates)
        #print(prevScore)
        #if i > 0 and j > 0 and distance[i-1][j-1] == prevScore:
            #mapping.append([target[i],source[j]])
            #i -= 1
            #j -= 1
        #elif i > 0 and distance[i-1][j] == prevScore:
            #mapping.append([target[i],'.'])
            #i -= 1
        #elif j > 0 and distance[i][j-1] == prevScore:
            #mapping.append(['.',source[j]])
            #j -= 1
    #if i == 0 and j == 0:
        #mapping.append([target[i],source[j]])
    #print(i,j)
    #if i > 0:
        #while i > 0:
            #mapping.append([target[i],'.'])
            #i -= 1
    #if j  > 0:
        #while j > 0:
            #mapping.append(['.',source[j]])
            #j -= 1
    #mapping.reverse()
    #return distance[n][m],mapping

def DTW(firstTrans,secondTrans,costs=None,distOnly=True):
    distMat = np.zeros((len(firstTrans),len(secondTrans)))
    distMat[0][0] = getCost(firstTrans[0],secondTrans[0],costs)
    for i in xrange(1,len(firstTrans)):
        distMat[i][0] = distMat[i-1][0] + getCost(firstTrans[i],secondTrans[0],costs)
    for j in xrange(1,len(secondTrans)):
        distMat[0][j] = distMat[0][j-1] + getCost(firstTrans[0],secondTrans[j],costs)
    for i in xrange(1,len(firstTrans)):
        for j in xrange(1,len(secondTrans)):
            prevScore = min([distMat[i][j-1],distMat[i-1][j-1],distMat[i-1][j]])
            distMat[i][j] = prevScore + getCost(firstTrans[i],secondTrans[j],costs)
    if distOnly:
        return distMat[len(firstTrans)-1][len(secondTrans)-1]
    mapping = []
    i = len(firstTrans)-1
    j = len(secondTrans)-1
    while i > -1 and j > -1:
        prevScore = min([distMat[i][j-1],distMat[i-1][j-1],distMat[i-1][j]])
        if distMat[i-1][j-1] == prevScore:
            mapping.append([firstTrans[i],secondTrans[j]])
            i -= 1
            j -= 1
        elif distMat[i-1][j] == prevScore:
            mapping.append([firstTrans[i],'.'])
            i -= 1
        elif distMat[i][j-1] == prevScore:
            mapping.append(['.',secondTrans[j]])
            j -= 1
    if i != -1:
        for m in range(i,-1,-1):
            mapping.append([firstTrans[m],'.'])
    if j != -1:
        for m in range(j,-1,-1):
            mapping.append(['.',secondTrans[m]])
    mapping.reverse()
    return distMat[len(firstTrans)-1][len(secondTrans)-1],mapping

def dtw_distance(source,target):
    distMat = generate_distance_matrix(source,target)
    return regularDTW(distMat)

def generate_distance_matrix(source,target):
    sLen = source.shape[0]
    tLen = target.shape[0]
    distMat = np.zeros((sLen,tLen))
    for i in range(sLen):
        for j in range(tLen):
            distMat[i,j] = euclidean(source[:,i],target[:,j])
    return distMat

def regularDTW(distMat,distOnly=True):
    sLen,tLen = distMat.shape
    
    totalDistance = np.zeros(sLen+1,tLen+1)
    totalDistance[0,:] = np.inf
    totalDistance[:,0] = np.inf
    totalDistance[0,0] = 0
    totalDistance[1:sLen+1,1:tLen+1] = distMat
    
    minDirection = np.zeros(sLen+1,tLen+1)
    
    for i in range(sLen):
        for j in range(tLen):
            minPrevDistance, direction = min(enumerate([totalDistance[i,j],totalDistance[i,j+1],totalDistance[i+1,j]]), key=operator.itemgetter(1))
            totalDistance[i+1,j+1] = totalDistance[i+1,j+1] + minPrevDistance
            minDirection[i,j] = direction
    
    if distOnly:
        return totalDistance[sLen,tLen]
    
    mapping = zeros(max([sLen,tLen])*2,2)
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
        
            

#def spareDTW(seriesOne,seriesTwo):
    #distExp = 2
    #res = 0.3
    #seriesOne = np.array(seriesOne)
    #seriesTwo = np.array(seriesTwo)
    #oneLen = len(seriesOne)
    #twoLen = len(seriesTwo)
    #distMat = np.zeros(signalLen,tempLen)
    #UB = res
    #LB = 0
    #while LB < 1-res/2
        #idxO = ((min_value < seriesOne) & (seriesOne < max_value)).nonzero()[0]
        #idxT = find(temp > LB & temp < UB);
        #idxT = ((min_value < seriesTwo) & (seriesTwo < max_value)).nonzero()[0]
        #for iS = 1, length(idxS):
            #for iT = 1:length(idxT):
                #dist = (signal(idxS(iS)) - temp(idxT(iT)))^ distExp
                #if dist == 0:
                    #dist = -1
                #distMat(idxS(iS),idxT(iT)) = dist
        #LB = LB + res/2
        #UB = LB + res
    #for i = 1:signalLen:
           #for j = 1:tempLen:
               #if ~distMat(i,j)
                   #continue;
               #end
               #if i > 1 and j > 1:
                   #lowNeigh = [distMat(i-1,j-1) distMat(i-1,j) distMat(i, j-1) ]
               #elif i > 1:
                   #lowNeigh = distMat(i-1,j)
               #elif j > 1:
                   #lowNeigh = distMat(i, j-1)
               #else:
                   #lowNeigh = -1
               #minDist = min(lowNeigh)
               #if minDist == -1:
                   #minDist = 0
               #if distMat(i,j) == -1:
                   #distMat(i,j) = 0
               #distMat(i,j) = distMat(i,j) + minDist;
               #if i <  signalLen && j < tempLen
                   #if ~any([distMat(i+1,j+1) distMat(i+1,j) distMat(i, j+1) ])
                       #distMat(i+1,j+1) = (signal(i+1) - temp(j+1))^ distExp;
                       #distMat(i+1,j) = (signal(i+1) - temp(j))^ distExp;
                       #distMat(i, j+1) = (signal(i) - temp(j+1))^ distExp;
                   #end
               #elseif i <  signalLen
                   #if ~ distMat(i+1,j)
                       #distMat(i+1,j) = (signal(i+1) - temp(j))^ distExp;
                   #end
               #elseif j < tempLen
                   #if ~distMat(i, j+1)
                       #distMat(i, j+1) = (signal(i) - temp(j+1))^ distExp;
                   #end
               #end
                   
           #end
    #end
    
    #dist = (distMat(signalLen,tempLen)) ^ (1/distExp);
