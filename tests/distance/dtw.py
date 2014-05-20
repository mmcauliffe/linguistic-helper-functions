
from numpy import array
import unittest
from linghelper.distance.dtw import dtw_distance,generate_distance_matrix

class DTWTest(unittest.TestCase):
    def setUp(self):
        self.source = array([[2,3,4],
                            [5,6,7],
                            [2,7,6],
                            [1,5,6]])
        self.target = array([[5,6,7],
                            [2,3,4],
                            [6,8,3],
                            [2,7,9],
                            [1,5,8],
                            [7,4,9]])
    
    def test_dtw(self):
        distmat = generate_distance_matrix(self.source, self.target)
        print(distmat)
        linghelper = dtw_distance(self.source,self.target)
        
        print(linghelper)
        dist = 24.9
        print(dist)
        self.assertTrue(dist == linghelper)
        
if __name__ == '__main__':
    unittest.main()
    
