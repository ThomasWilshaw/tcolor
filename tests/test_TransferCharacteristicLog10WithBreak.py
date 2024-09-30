import unittest
from tcolour import transfer_characteristic as TC

class TestTransferCharacteristicLog10WithBreak(unittest.TestCase):
    def setUp(self) -> None:
        self.TCL = TC.TransferCharacteristicLog10WithBreak(parameters=
                                                           {'a': 5.555556,
                                                            'b': 0.052272,
                                                            'c': 0.24719,
                                                            'd': 0.385537,
                                                            'e': 5.367655,
                                                            'f': 0.092809,
                                                            'h': 0.010591}
                                                            )
        
    def test_forward_transfer(self):
        data = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 10.0, 20.0, 30.0]
        out = self.TCL.forward_transfer(data)

        check = [0.14648555, 0.332089681, 0.401783016, 0.443691022, 0.473755371, 0.497215986, 0.516457813, 0.532769346, 0.546926248, 0.559431892, 0.570631558, 0.816917159, 0.891278295, 0.934789465]

        for id, idx in enumerate(check):
            self.assertAlmostEqual(out[id], idx)

    def test_inverse_transfer(self):
        data = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        out = self.TCL.inverse_transfer(data)

        check = [-0.015427407, 0.001339691, 0.022557012, 0.071731042, 0.196550678, 0.513383396, 1.317607586, 3.358989402, 8.540678494, 21.6934859, 55.0795767]

        for id, idx in enumerate(check):
            self.assertAlmostEqual(out[id], idx)

    def test_roundtrip(self):
        data = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 10.0, 20.0, 30.0]
        forward = self.TCL.forward_transfer(data)

        inverse = self.TCL.inverse_transfer(forward)

        for id, idx in enumerate(inverse):
            self.assertAlmostEqual(data[id], idx, 13)

