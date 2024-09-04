from enum import Enum
from TransferCharacteristic import *

class RGBPrimaries():
    """Defines a set of three RGB primaries using the CIE xy coordinate system."""

    def __init__(self, r=[], g=[], b=[]) -> None:
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self) -> str:
        return "RGBPrimaries(r=%r, g=%r, b=%r)" % (self.r, self.g, self.b)
    
class CIEVersion(Enum):
    CIE_1931_2_DEGREE = 1
    CIE_2015_2_DEGREE = 2
    


class Colourimetry:
    """Holds all the data required to define a colour space\n
    Attributes:\n
        descriptor:                 A unique identifying key.
        primaries:                  An array defining a set of three RGB primaries using the CIE xy coordinate system.
        achromatic:                 A single array defining a pair of CIE xy coordinates.
        transfer_characteristic:    Either a file, parametric function or named function.
        hints:                      Dictionary providing ancillary colourimetric information.
        alias:                      An array of strings representing aliases for the chosen descriptor.
        cie_version:                An enum of predefined CIE versions 

    """
    def __init__(self, descriptor:str="", rgb_primaries:RGBPrimaries=RGBPrimaries(), achromatic:list=[], 
                 transfer_characteristic:TransferCharacteristic=None, hints:list=[], alias:list=[],
                 cie_version:CIEVersion=None) -> None:
        self.descriptor = descriptor
        self.primaries = rgb_primaries
        self.achromatic = achromatic
        self.transfer_characteristic = transfer_characteristic
        self.hints = hints
        self.alias = alias
        self.cie_version = cie_version

    def __repr__(self) -> str:
        return "Colourimetry(descriptor=%r,primaries=%r, achromatic=%r, transfer_characteristic=%r, hints=%r, alias=%r, cie_version=%r)" \
            % (self.descriptor, self.primaries, self.achromatic, self.transfer_characteristic, self.hints, self.alias, self.cie_version)


if __name__ == "__main__":
    col = Colourimetry()
    print(col.__doc__)

    col.descriptor = "sRGB"

    col.primaries.r = [0.64, 0.33]
    col.primaries.g = [0.3, 0.6]
    col.primaries.b = [0.15, 0.06]

    col.achromatic = [0.3127, 0.329]

    col.transfer_characteristic = TransferCharacteristicPower(parameters={'a': 2.2})
    col.hints.append("value")
    col.alias.append("value")

    col.cie_version = CIEVersion.CIE_1931_2_DEGREE

    print(repr(col))

