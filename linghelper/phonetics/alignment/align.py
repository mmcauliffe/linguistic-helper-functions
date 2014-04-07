import subprocess
import os
import sys
import re
import shutil
from scipy.io import wavfile
from scipy.signal import resample

sr_model = 16000

htk_root = ''
from linghelper.settings import HMM_MODEL_DIR as hmm_dir
if hmm_dir == '' or not os.path.exists(hmm_dir):
    raise(ImportError('Please specify a HMM_MODEL_DIR variable as the absolute path to a directory containing HMM models in a linghelper_settings.py file located on your path'))
tmp_dir = os.path.join(hmm_dir,'tmp')

def prep_wav(wav_path,output_path):
    SR, sig = wavfile.read(wav_path)
    
    if SR == sr_model:
        shutil.copy2(wav_path,output_path)
    elif SR > sr_model:
        new_num_samples = int(len(sig) * sr_model/ SR)
        newsig = resample(sig,new_num_samples)
        wavfile.write(output_path,sr_model,newsig)
    else:
        raise Exception("File currently needs to be sampled at or above 16000")

def prep_mlf(transcript):
    # Read in the dictionary to ensure all of the words
    # we put in the MLF file are in the dictionary. Words
    # that are not are skipped with a warning.
    dictionary_path = os.path.join(hmm_dir,'dict')
    dictwords = set([]) # build hash table
    with open(dictionary_path,'r') as f:
        for line in f.readlines():
            if line != "\n" and line != "" :
                dictwords.update([line.split()[0]])
    
    lines = transcript.split()
    pause = 'sp'
    words = [pause]


    # this pattern matches hyphenated words, such as TWENTY-TWO; however, it doesn't work with longer things like SOMETHING-OR-OTHER
    hyphenPat = re.compile(r'([A-Z]+)-([A-Z]+)')

    for l in lines:
        txt = l.strip()
        txt = txt.replace('{breath}', '{BR}').replace('&lt;noise&gt;', '{NS}')
        txt = txt.replace('{laugh}', '{LG}').replace('{laughter}', '{LG}')
        txt = txt.replace('{cough}', '{CG}').replace('{lipsmack}', '{LS}')

        for pun in [',', '.', ':', ';', '!', '?', '"', '%', '(', ')', '--', '---']:
            txt = txt.replace(pun,  '')

        txt = txt.upper()

        # break up any hyphenated words into two separate words
        txt = re.sub(hyphenPat, r'\1 \2', txt)

        txt = txt.split()

        for wrd in txt:
            if (wrd in dictwords):
                words.append(wrd)
                words.append(pause)
            else:
                print("SKIPPING WORD", wrd)


    return words
    
    


def readAlignedMLF(mlfoutput):
    # This reads a MLFalignment output  file with phone and word
    # alignments and returns a list of words, each word is a list containing
    # the word label followed by the phones, each phone is a tuple
    # (phone, start_time, end_time) with times in seconds.
    
    lines = [l.rstrip() for l in mlfoutput.split('\n')]
    if len(lines) < 3 :
        raise ValueError("Alignment did not complete succesfully.")
            
    j = 2
    ret = []
    while (lines[j] != '.'):
        if (len(lines[j].split()) == 5): # Is this the start of a word; do we have a word label?
            # Make a new word list in ret and put the word label at the beginning
            wrd = lines[j].split()[4]
            ret.append([wrd])
        
        # Append this phone to the latest word (sub-)list
        ph = lines[j].split()[2]
        st = float(lines[j].split()[0])/10000000.0 + 0.0125
        en = float(lines[j].split()[1])/10000000.0 + 0.0125   
        if st < en:
            ret[-1].append([ph, st, en])
        
        j += 1
        
    return ret

def prep_working_directory(name) :
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

    

    
def align(wav_path,transcript):
    surround_token = "sp" 
    between_token = "sp" 
    wav_name = os.path.split(wav_path)[1]
    name = wav_name[:-4]
    temp_path = os.path.join(tmp_dir,wav_name)
    
    input_mlf = os.path.join(tmp_dir,'%s-tmp.mlf' % name)
    
    # create working directory
    prep_working_directory(name)
    
    
    
    #prepare wavefile: do a resampling if necessary
    prep_wav(wav_path,temp_path)
    
    
    #prepare mlfile
    words = prep_mlf(transcript)
    
    with open(input_mlf, 'w') as fw:
        fw.write('#!MLF!#\n')
        fw.write('"*/%s-tmp.lab"\n' % name)
        for wrd in words:
            fw.write(wrd + '\n')
        fw.write('.\n')
 
    codetr = os.path.join(tmp_dir,'%s-codetr.scp' % name)
    testscp = os.path.join(tmp_dir,'%s-test.scp' % name)
    testplp = os.path.join(tmp_dir,'%s-tmp.plp' % name)
    #prepare scp files
    with open(codetr, 'w') as fw:
        fw.write(wav_path + ' %s\n' % testplp)
    with open(testscp, 'w') as fw:
        fw.write(' %s\n' % testplp)
    
    # generate the plp file using a given configuration file for HCopy
    com = [os.path.join(htk_root,'HCopy'),'-T','1',
            '-C',os.path.join(hmm_dir , 'config'),
            '-S',codetr]
    subprocess.call(com)
    
    # run Verterbi decoding
    com = [os.path.join(htk_root,'HVite'),'-T','1','-a','-m','-I',input_mlf,
            '-H',os.path.join(hmm_dir ,'macros'),'-H',os.path.join(hmm_dir,'hmmdefs'),
            '-S', testscp,'-i', os.path.join(tmp_dir,'%s-aligned.mlf' % name),'-p','0.0','-s',
            '5.0',os.path.join(hmm_dir,"dict"), os.path.join(hmm_dir,'monophones')]
    p = subprocess.Popen(com,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    stdout, stderr = p.communicate()
   # output_mlf = str(stdout.decode())
    with open(os.path.join(tmp_dir,'%s-aligned.mlf' % name),'r') as f:
        output_mlf = f.read()
    return readAlignedMLF(output_mlf)

def extract_info(alignment):
    words = alignment[1:-1]
    begin = 0
    vowels = []
    for w in words:
        if w[0] == 'sp':
            continue
        if begin == 0:
            begin = w[1][1]
        for p in w[1:]:
            if p[0].endswith('1') or p[0].endswith('2') or p[0].endswith('0'):
                vowels.append(p)
    end = words[-1][-1][-1]
    return begin,end,vowels

if __name__ == '__main__':
    wavname = '/media/Data/Corpora/ATI/Model/Female/225/f_subj225_a_cot.wav'
    print(align(wavname,'cot'))
    print(extract_info(align(wavname,'cot')))
