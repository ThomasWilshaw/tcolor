import unittest
from tcolour import TransferCharacteristic as TC

class TestTransferCharacteristicPowWithBreak(unittest.TestCase):
    def setUp(self) -> None:
        self.TCP = TC.TransferCharacteristicPowWithBreak(parameters={"a": 1.055, "b": -0.055, "c": 12.92, "d": 0.0031308, "g": 2.4})


    def test_forward_transfer(self):
        data = [0.0, 0.1, 0.5, 1.0]
        out = self.TCP.forward_transfer(data)

        check = [0.0]+[1.055*(pow(x, 1.0/2.4))-0.055 for x in data[1:]]

        self.assertListEqual(out, check)

    def test_inverse_transfer(self):
        data = [0.0, 0.1, 0.5, 1.0]
        forward = self.TCP.forward_transfer(data)
        inverse = self.TCP.inverse_transfer(forward)

        self.assertListEqual(data, inverse)