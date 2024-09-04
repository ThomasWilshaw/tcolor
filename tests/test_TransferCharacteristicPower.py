import unittest
from tcolour import TransferCharacteristic as TC

class TestTransferCharacteristicPower(unittest.TestCase):
    def setUp(self) -> None:
        self.TCP = TC.TransferCharacteristicPower(parameters={'a': 2.2})

    def test_forward_transfer(self):
        data = [0.0, 0.1, 0.5, 1.0]
        out = self.TCP.forward_transfer(data)

        check = [pow(x, self.TCP.parameters["a"]) for x in data]

        self.assertListEqual(out, check)

    def test_inverse_transfer(self):

        data = [0.0, 0.1, 0.5, 1.0]
        out = self.TCP.inverse_transfer(data)

        check = [pow(x, 1.0/self.TCP.parameters["a"]) for x in data]

        self.assertListEqual(out, check)

