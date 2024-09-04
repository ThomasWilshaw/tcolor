import unittest
from tcolour import TransferCharacteristic as TC

class TestTransferCharacteristicPow(unittest.TestCase):
    def test_forward_transfer(self):
        TCP = TC.TransferCharacteristicPow(TC.TransferCharacteristicType.PARAMETRIC, parameters={'a': 2.2})

        data = [0.0, 0.1, 0.5, 1.0]
        out = TCP.forward_transfer(data)

        check = [pow(x, TCP.parameters["a"]) for x in data]

        self.assertListEqual(out, check)

    def test_inverse_transfer(self):
        TCP = TC.TransferCharacteristicPow(TC.TransferCharacteristicType.PARAMETRIC, parameters={'a': 2.2})

        data = [0.0, 0.1, 0.5, 1.0]
        out = TCP.inverse_transfer(data)

        check = [pow(x, 1.0/TCP.parameters["a"]) for x in data]

        self.assertListEqual(out, check)

