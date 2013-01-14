import numpy as np

from .media.constants import costs as FIXED_COSTS

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

def getCost(segOne,segTwo,costs=None):
    if segOne == segTwo:
        return 0.0
    if costs is not None:
        if (segOne,segTwo) in costs:
            return costs[(segOne,segTwo)]
        return 2.0
    if (segOne,segTwo) in FIXED_COSTS:
        return FIXED_COSTS[(segOne,segTwo)]
    return 2.0
