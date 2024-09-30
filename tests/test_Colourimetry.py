import unittest
import sys
from .context import tc

class TestColourimetry(unittest.TestCase):
    def test_valid(self):
        col = tc.Colourimetry.Colourimetry()
        # Should be invalid as nothing is set
        self.assertFalse(col.colourspace_valid())

        col.primaries.r = [0.64, 0.33]
        col.primaries.g = [0.3, 0.6]
        col.primaries.b = [0.15, 0.06]
        # Should be invalid as it is missing achromatic and TC
        self.assertFalse(col.colourspace_valid())

        col.achromatic = [0.3127, 0.329]
        # Should be invalid as still missing TC
        self.assertFalse(col.colourspace_valid())

        col.transfer_characteristic = tc.TransferCharacteristic.TransferCharacteristicPower(parameters={'a': 2.2})
        self.assertTrue(col.colourspace_valid())