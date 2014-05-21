import unittest
from linghelper.phonetics.representations.segments import to_segments
from numpy import array


class MfccTest(unittest.TestCase):
    def setUp(self):
        self.mfcc = array([[-12.6431900383024, -4.11124978708355, -8.39927505519070, -6.84749105388128, -6.85480312211548, -6.05639283075425, -6.59116209025136, -6.35550982517426, -3.41832566686831, -4.02182931281004, -2.65106705926123, -2.99819940508193, -2.30778514645189, -0.411632061457631, 0.625942602749560, 1.28149015576795, 1.29554681707301, 0.279062976842321, -0.265134940453222, -0.000248053411330993, 0.337039789375566, 3.76480993916839, 2.94008605165846, 2.12280963860397, -3.44612000860328, -4.11686023199763, -5.39123409196919, -1.41150958907003, -2.49255623276504, -4.95460784580001],
[-4.05730021228181, 3.92852555480955, 5.97305669246826, 6.73321058743357, 7.44647449033269, 7.34587813963090, 7.85789022883109, 7.73397667062598, 4.56902248959431, -0.677525529611384, -5.09549389629633, -5.49150685084000, -8.63611601408430, -10.8406453346777, -12.1549505432557, -12.7888930397252, -13.3747168154787, -16.2591043297242, -15.6068850598847, -17.2451502427959, -16.1241611563671, -13.1899621044646, -11.6878292171303, -6.29034358052595, -12.4686978506948, -19.0762518534413, -22.8968673554816, -9.11343244281742, -1.90886513725121, 7.29138348727605],
[22.0306798265591, 22.0760813005152, 23.3516727681497, 25.1953774572909, 26.5397990303092, 24.2265155035167, 20.9841288446810, 17.6883544752606, 15.3772029902501, 15.5681982020768, 16.4495661008059, 15.5610610852308, 14.9612154376887, 14.1500647008950, 13.0349848269350, 9.08297847638858, 10.9361098591242, 12.8960761787767, 9.26804001362959, 9.23310014183982, 12.0186221239960, 9.54537218465689, 6.42060002651409, 17.5015862847899, 24.6696311931783, 19.8483915626917, 16.8612031100367, 12.6642576673037, 11.4325779133121, 21.0034330136751],
[-27.2535889687542, -35.2417066965514, -38.3226019423256, -34.7832732130129, -35.8250042773585, -35.0097116025137, -32.7444144700091, -32.1075358276230, -33.2418403954548, -28.4001168531173, -26.2873950313471, -24.5364232237130, -21.7520222976323, -20.1179259649045, -21.6203032799415, -18.5385523039657, -16.1161506870567, -16.1508485273020, -11.9159153515956, -13.7359348596800, -8.00734179306039, -2.11674943937257, 1.66097121482712, 4.24184370448343, 14.7360490803912, 12.6013322213738, 18.5548529475507, 8.00322599407388, 7.44136706113861, 8.36626451431917],
[-19.8791732884552, -30.2474328454546, -24.3900294502569, -28.0029907788255, -29.0459289296974, -26.1950382483364, -22.4561726287780, -18.8283346826904, -16.6106508134513, -25.9916790008025, -21.4478323602466, -18.5310723442777, -17.4009263471459, -17.7948609151450, -12.7048530638342, -14.4513647432306, -17.8353846613736, -13.5030481872956, -8.85633924487078, -9.83602417498314, -9.76431907793327, -10.5068628164658, -5.39868318768174, -2.80272277416321, 4.38954795334307, 3.00598203613582, 4.38119851311758, 6.70942973453174, 8.49117751576336, -1.81554840440983],
[1.32966283838449, -12.9985003008692, -8.04316645864802, -7.59042000662015, -10.2852812635049, -11.6164027935889, -16.6525486752631, -19.3219555214239, -19.8759839497387, -11.1350471374046, -12.9378920581037, -15.0980574039333, -12.6825365412094, -11.2463148398999, -13.6004132487233, -9.53103695462074, -4.85170424488302, -8.64247373383929, -7.81543651457696, -3.60894147622008, -0.232435182297726, 4.37377502009800, -1.30249791519882, 3.95961779700153, 10.4319863921451, 11.3510889560315, 14.8226036062117, 6.11493591857146, 12.0323851786871, 9.88998037757504],
[5.56498747234649, 6.17974065495386, 8.74639267446779, 12.9004637892936, 13.7825918141741, 14.1010792710966, 15.0185907686574, 16.2640607870346, 16.5743639929129, 18.7741954858544, 19.7244438072630, 24.1188660027892, 20.1872722973683, 23.0212315658774, 26.4012333215658, 21.1713302522291, 26.2641230570127, 22.5513619687369, 21.6062832133461, 19.1393604902652, 15.4441506826413, 9.55658070237957, 11.0089008917499, 4.09801436844764, -2.09733336896730, -1.20944738980806, -10.9200519932826, -11.3372902317157, -3.69976167168993, -3.26912993561542],
[-10.9153495926642, -21.1434766312004, -28.5389290236827, -27.32164744135402, -21.1735383679980, -17.5556436251888, -16.9450757387432, -16.5496467363008, -12.4367915728882, -19.7167250380373, -15.3162704799224, -18.0219477203364, -14.5366663897389, -14.5730817427552, -13.0486804896353, -2.65717858243729, -12.3512834494283, -5.73081365145198, -1.14357809015832, -0.283525537859710, 2.67873401219133, -3.93221723974886, -2.40589288811884, 0.634704507909726, -0.136704576997914, 0.546617744530202, 14.3816061204296, 13.2000877644548, -0.701061434018668, 6.22290592889300],
[7.63999462223566, 3.28509323328750, 10.3231983363384, 16.9981773095089, 11.6503361574799, 7.00891315382914, 14.0646046774172, 15.0115800596872, 11.1919279394408, 14.8282482754650, 7.43429808890402, 6.03801466946697, 5.15580572251729, 7.89323142352018, 4.65959802389136, 0.366780874993051, 10.1170843502941, 3.51623744966968, 3.11339352181777, -2.40736284129219, -6.51263978030173, -1.25642443788842, -7.11750182735345, -13.0832617130400, 2.98548951618758, 1.25527492543389, 12.2320840412696, 5.64438448548424, 4.43791536288697, -0.434165430041457],
[0.373716538623152, -6.62965757557485, -16.5092881621301, -21.0992730280629, -20.4609651648216, -12.7298062150581, -18.4196560006050, -10.5920322822895, -9.41600245822621, -11.9569334992839, -7.91868052324521, -10.1726402630870, -9.30256422374479, -15.1870511639641, -13.2688157069128, -19.7632580764917, -23.8643799558447, -22.3723092771984, -28.4977778627909, -28.6850505208693, -24.7917075615466, -27.7105208258874, -22.3597708013816, -22.5551348781499, -17.3131153594454, -12.8282169680205, -19.5892973500126, -16.6483062602605, 5.67960237302644, 4.67088909829900],
[-0.675238025032723, -7.11061387431964, -5.17508446842980, -10.5212212424821, -13.9805489146265, -13.0061255295009, -3.64179395901407, -7.91220410028818, -4.00798644588149, 0.879635385743963, -1.92576390229584, -0.945979929033468, -8.03356167639994, -8.19428854317041, -9.71472510299975, -3.36371354773745, -9.07884965960712, -8.51285161791480, -2.18590648310040, -4.94417508499088, -12.4482627686985, -11.0186159837084, -13.5392266043389, -4.01147231787475, -6.68541157507647, 1.15077006378276, 4.36083825903835, -0.0784899881400669, 2.39120487305976, 6.96171151639114],
[-6.13712683890103, -16.4927199016897, -20.0860315069963, -18.4941511304746, -14.5817833836632, -17.0004302747678, -23.0626149594185, -25.4933397070600, -25.6098187418918, -26.7680163388017, -25.6837265697137, -24.1669783698173, -15.2342441407717, -8.79764589747416, -10.0669535117613, -15.7704813653120, -6.08710629242132, -4.97639281300427, -8.27492379405294, -5.95022483646383, -4.16756615405278, -4.59388534133343, 2.09293761452189, 4.04413716017460, 4.15034451697720, 5.02532196424412, 7.37755061519176, 8.72889651641524, -2.19735786739655, -6.72737187527193]])
    
    
    def test(self):
        expected = array([1,13,21,25])
        print(self.mfcc.shape)
        segStart = to_segments(self.mfcc.T)
        print(segStart)
        print(expected)
        self.assertEqual(segStart,expected)
        
if __name__ == '__main__':
    unittest.main()