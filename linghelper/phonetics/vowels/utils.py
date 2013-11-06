from praatinterface import PraatLoader

def extract_vowel(original_file,begin,end,output_file):
    begin -= 0.025
    end += 0.025
    p = PraatLoader()
    p.run_script('extract.praat',*args)
