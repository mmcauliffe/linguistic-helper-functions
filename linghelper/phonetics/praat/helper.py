from numpy import array
import re

def to_array(in_string):
    lines = in_string.split('\n')
    output = []
    for l in lines:
        output.append(map(float,l.split('\t')))
    return array(output)

def to_time_based_dict(praat_output,remove_undefined = False):
    lines = praat_output.splitlines()
    head = re.sub('[(]\w+[)]','',lines.pop(0))
    head = head.split("\t")[1:]
    output = {}
    for l in lines:
        if '\t' in l:
            line = l.split("\t")
            time = line.pop(0)
            values = {}
            for j in range(len(line)):
                if remove_undefined and line[j] == '--undefined--':
                    continue
                v = line[j]
                if v != '--undefined--':
                    v = float(v)
                values[head[j]] = v
            if values:
                output[float(time)] = values
    return output