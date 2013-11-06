import numpy as np

from .media.constants import costs as FIXED_COSTS

def  minEditDist(target, source,distOnly=False):
    ''' Computes the min edit distance from target to source. Figure 3.25 '''
    def insertCost(seg):
        return 1

    def deleteCost(seg):
        return 1

    def substCost(segone,segtwo):
        if segone == segtwo:
            return 0
        segone = segone.upper()
        segtwo = segtwo.upper()
        if (segone,segtwo) in costs:
            return costs[(segone,segtwo)]
        if (segtwo,segone) in costs:
            return costs[(segtwo,segone)]
        return 2

    n = len(target)
    m = len(source)

    distance = [[0 for i in range(m+1)] for j in range(n+1)]

    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + insertCost(target[i-1])

    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + deleteCost(source[j-1])

    for i in range(1,n+1):
        for j in range(1,m+1):
            distance[i][j] = min(distance[i-1][j]+1,
                                distance[i][j-1]+1,
                                distance[i-1][j-1]+substCost(source[j-1],target[i-1]))
    if distOnly:
        return distance[n][m]
    #alignment
    i = n-1
    j = m-1
    mapping = []
    prevScore = min([distance[i][j-1],distance[i-1][j-1],distance[i-1][j]])
    if distance[i-1][j-1] == prevScore:
        mapping.append([target[i],source[j]])
    elif distance[i-1][j] == prevScore:
        mapping.append([target[i],'.'])
    elif distance[i][j-1] == prevScore:
        mapping.append(['.',source[j]])
    while i > 0 and j > 0:
        prevScore = min([distance[i][j-1],distance[i-1][j-1],distance[i-1][j]])
        if distance[i-1][j-1] == prevScore:
            mapping.append([target[i],source[j]])
            i -= 1
            j -= 1
        elif distance[i-1][j] == prevScore:
            mapping.append([target[i],'.'])
            i -= 1
        elif distance[i][j-1] == prevScore:
            mapping.append(['.',source[j]])
            j -= 1
    if i == 0 and j == 0:
        mapping.append([target[i],source[j]])
    if i > 0:
        while i > 0:
            mapping.append([target[i],'.'])
            i -= 1
    if j  > 0:
        while j > 0:
            mapping.append(['.',source[j]])
            j -= 1
    mapping.reverse()
    return mapping

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

