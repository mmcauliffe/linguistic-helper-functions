
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
    
    def test_dtw_unnorm(self):
        distmat = generate_distance_matrix(self.source, self.target)
        linghelper = dtw_distance(self.source,self.target,norm=False)
        
        r_dtw_output = 31.14363
        print(linghelper)
        self.assertTrue(abs(r_dtw_output - linghelper) < 0.01)
    
    def test_dtw_norm(self):
        distmat = generate_distance_matrix(self.source, self.target)
        linghelper = dtw_distance(self.source,self.target,norm=True)
        
        r_dtw_output = 3.114363
        print(linghelper)
        self.assertTrue(abs(r_dtw_output - linghelper) < 0.01)
        
if __name__ == '__main__':
    unittest.main()
    
