import subprocess

SEM_PRED = '/home/michael/dev/Tools/SemPredScripts/SemPred.pl'

def getSemanticRelatedness(word,context,debug=False,style='A'):
    com = ["perl",SEM_PRED,word,','.join(context)]
    p = subprocess.Popen(com,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if debug:
        print stdout
        print stderr
    if stdout == '':
        return 0.0
    sp = stdout.split(",")
    spsum = sum(map(float,sp))
    if style == 'A':
        if spsum > 0:
            return spsum / float(len(sp))
        return 0.0
    return spsum
