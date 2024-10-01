import unittest
from tcolour import config
from tcolour import transfer_characteristic as tc
from tcolour import colourimetry

class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.conf = config.Config()

    def test_add_complete_colourimetry_from_file(self):
        self.conf.add_colourimetry("tests//files//complete_colourimetry_set.yaml")

        colourimetry = self.conf.get_colourimetry("Complete bogus set")

        self.assertEqual(colourimetry.descriptor, "Complete bogus set")

        self.assertEqual(colourimetry.primaries.r, [0.640, 0.330])
        self.assertEqual(colourimetry.primaries.g, [0.3, 0.6])
        self.assertEqual(colourimetry.primaries.b, [0.15, 0.06])

        self.assertEqual(colourimetry.achromatic, [0.3127, 0.3290])

        self.assertTrue(isinstance(colourimetry.transfer_characteristic, tc.TransferCharacteristicPower))
        self.assertEqual(colourimetry.transfer_characteristic.parameters["a"], 2.2)

        self.assertEqual(colourimetry.hints[0], "Hint")
        self.assertEqual(colourimetry.hints[1], "Other hint")

        self.assertEqual(colourimetry.alias[0], "sRGB")

        self.assertEqual(colourimetry.cie_version, "CIE_1931_2_DEGREE")

    def test_add_complete_colourimetry_from_object(self):
        col = colourimetry.Colourimetry()
        col.descriptor = "Set"
        col.primaries.r = [0.640, 0.330]
        col.primaries.g = [0.3, 0.6]
        col.primaries.b = [0.15, 0.06]
        col.achromatic = [0.3127, 0.3290]
        col.transfer_characteristic = tc.TransferCharacteristicPower(parameters={"a": 2.5})
        col.hints = ["hint"]
        col.alias = ["set2"]
        col.cie_version = "CIE_1931_2_DEGREE"

        self.conf.add_colourimetry(col)

        col2 = self.conf.get_colourimetry("Set")

        self.assertEqual(col2.descriptor, "Set")

        self.assertEqual(col2.primaries.r, [0.640, 0.330])
        self.assertEqual(col2.primaries.g, [0.3, 0.6])
        self.assertEqual(col2.primaries.b, [0.15, 0.06])

        self.assertEqual(col2.achromatic, [0.3127, 0.3290])

        self.assertTrue(isinstance(col2.transfer_characteristic, tc.TransferCharacteristicPower))
        self.assertEqual(col2.transfer_characteristic.parameters["a"], 2.5)

        self.assertEqual(col2.hints[0], "hint")

        self.assertEqual(col2.alias[0], "set2")

        self.assertEqual(col2.cie_version, "CIE_1931_2_DEGREE")

    def test_add_complete_colourimetry_from_stream(self):
        stream = """
- Complete bogus set:
    RGB Primaries: {
        Red: {x: 0.640, y: 0.330},
        Green: {x: 0.300, y: 0.600},
        Blue: {x: 0.150, y: 0.060}
    }
    Achromatic Centroid: {x: 0.3127, y: 0.3290}
    Transfer Characteristic:
        - Type: Parametric
        - Function: power
        - Parameters: {
            a: 2.2
        }
    Hints:
        - Hint
        - Other hint
    Alias:
        - sRGB
    CIE Version: CIE_1931_2_DEGREE
        """

        self.conf.add_colourimetry(stream)
        colourimetry = self.conf.get_colourimetry("Complete bogus set")

        self.assertEqual(colourimetry.descriptor, "Complete bogus set")

        self.assertEqual(colourimetry.primaries.r, [0.640, 0.330])
        self.assertEqual(colourimetry.primaries.g, [0.3, 0.6])
        self.assertEqual(colourimetry.primaries.b, [0.15, 0.06])

        self.assertEqual(colourimetry.achromatic, [0.3127, 0.3290])

        self.assertTrue(isinstance(colourimetry.transfer_characteristic, tc.TransferCharacteristicPower))
        self.assertEqual(colourimetry.transfer_characteristic.parameters["a"], 2.2)

        self.assertEqual(colourimetry.hints[0], "Hint")
        self.assertEqual(colourimetry.hints[1], "Other hint")

        self.assertEqual(colourimetry.alias[0], "sRGB")

        self.assertEqual(colourimetry.cie_version, "CIE_1931_2_DEGREE")
