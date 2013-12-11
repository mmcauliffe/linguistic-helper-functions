import unittest
from .classes import Word

class SyllabificationTest(unittest.TestCase):
    def setUp(self):
        self.words = [['','B.AE.D'],
                    ['','B.AE.S.D.IY'],
                    ['','AH.B.AE.S.T.IY'],
                    ['','AH0.B.AE0.D.IY1']]
    def test_neighbours(self):
        w = Word(*self.words[0])
        self.assertEqual(w.neighbour_transcription('D','onset','final'),'D.AE.D')
        w = Word(*self.words[1])
        self.assertEqual(w.neighbour_transcription('D','onset','final'),'B.AE.S.D.IY')
        w = Word(*self.words[2])
        self.assertEqual(w.neighbour_transcription('D','onset','final'),'AH.B.AE.D.IY')
        w = Word(*self.words[3])
        self.assertEqual(w.neighbour_transcription('D','onset','final'),'AH0.B.AE0.D.IY1')


    def test_syllabification(self):
        w = Word(*self.words[0])
        self.assertEqual(w.segment_count('D'),1)
        w = Word(*self.words[1])
        self.assertEqual(w.segment_count('D'),1)
        w = Word(*self.words[2])
        self.assertEqual(w.segment_count('D'),0)
        w = Word(*self.words[3])
        self.assertEqual(w.segment_count('D'),1)
