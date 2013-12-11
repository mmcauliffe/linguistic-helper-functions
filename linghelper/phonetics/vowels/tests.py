import unittest
import os
from .formants import analyze_vowel

class FormantTest(unittest.TestCase):
    def setUp(self):
        self.test_path = '/home/michael/dev/Tools/Buckeye-12605.wav'

    def test_tracks(self):
        t = analyze_vowel(os.path.normpath(self.test_path),vowel='AE',foll_seg='D',prec_seg='B',speaker_gender='F')

