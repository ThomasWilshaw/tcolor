import unittest
from tcolour import transfer_characteristic as TC

class TestTransferCharacteristicSequence(unittest.TestCase):
    def setUp(self) -> None:
        self.TCS = TC.TransferCharacteristicSequence(
            [{'Descriptor': 'sRGB OETF', 'Direction': 'forward'},
             {'Descriptor': 'sRGB EOTF', 'Direction': 'inverse'}]
             )

    def test_forward_transfer(self):
        sequence = [{'Descriptor': 'sRGB OETF', 'Direction': 'forward'},
                    {'Descriptor': 'sRGB EOTF', 'Direction': 'inverse'}
                    ]
        
        self.assertListEqual(self.TCS.forward_transfer(), sequence)

    def test_inverse_transfer(self):
        sequence = [{'Descriptor': 'sRGB EOTF', 'Direction': 'inverse'},
                    {'Descriptor': 'sRGB OETF', 'Direction': 'forward'}
                    ]
        
        self.assertListEqual(self.TCS.inverse_transfer(), sequence)
    