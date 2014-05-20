from numpy import zeros,mean,std, sum, array
import copy

def summed_sq_error(features,segment_ends):
    num_segs = len(segment_ends)
    num_features = features.shape[1]
    seg_begin = 0
    sse = 0
    for l in range(1,num_segs):
        seg_end = segment_ends[l]
        ml = zeros((1,num_features))
        for t in range(seg_begin,seg_end):
            ml += features[t,:]
        ml = ml / (seg_end-seg_begin)
        for t in range(seg_begin,seg_end):
            sse += sum((features[t,:] - ml) ** 2)
        seg_begin = seg_end
    #print(sse)
    return sse

def to_segments(features):
    #print(features.shape)
    thresh = 0.15
    num_frames, num_coeffs = features.shape
    L = {}
    segment_iter = {}
    seg_temp = list(range(1,num_frames))
    for num_segments in range(num_frames-1,1,-1):
        #print(num_segments)
        best = []
        min_sse = 10000
        for l in range(num_segments-1):
            #print(min_sse)
            segment_set = copy.copy(seg_temp)
            
            if len(segment_set) == 0:
                continue
            del segment_set[l]
            #print(segment_set)
            sse = summed_sq_error(features,segment_set)
            if sse < min_sse:
                best = segment_set
                min_sse = sse
        if min_sse == 10000 and num_segments <= 2:
            continue
        segment_iter[num_segments] = best
        seg_temp = best
        L[num_segments] = min_sse
    Larray = array(list(L.values()))
    threshold = mean(Larray) + (thresh *std(Larray))
    #print(threshold)
    #print(segment_iter)
    #print(L)
    ks = list(segment_iter.keys())
    for i in range(max(ks),min(ks)-1,-1):
        #print(L[i])
        #print(i)
        if L[i] > threshold:
            optimal = segment_iter[i]
            break
    else:
        optimal = segment_iter[-1]
    #print(optimal)
    seg_begin = 0
    segments = zeros((len(optimal),num_coeffs))
    for i in range(len(optimal)):
        seg_end = optimal[i]
        segments[i,:] = mean(features[seg_begin:seg_end,:],axis=0)
        seg_begin = seg_end
    #print(segments)
    #raise(ValueError)
    return segments
