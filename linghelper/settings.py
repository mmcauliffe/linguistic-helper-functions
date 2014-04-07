

PRAAT_PATH = ''

HTK_PATH = ''

HMM_MODEL_DIR = ''

try:
    from linghelper_settings import *
except ImportError:
    import warnings
    warnings.warn("No linghelper_settings.py file detected in python path.  Some features may not work without specific settings defined in there.",warning.Warning)