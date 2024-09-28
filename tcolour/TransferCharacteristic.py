from enum import Enum
from math import log10
    
class TransferCharacteristic():
    """Defines a Transfer Characteristic, stored as either a URI, a Parametric or a Named function."""

    def __init__(self) -> None:
        pass

    def forward_transfer(self, data):
        """Processes data with the given characteristic transfer function in the forwards direction"""
        pass

    def inverse_transfer(self, data):
        """Processes data with the given characteristic transfer function in the inverse direction"""
        pass

    def valid(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "TransferCharacteristic()" 
    
class TransferCharacteristicParametric(TransferCharacteristic):
    """A parametric transfer function."""

    def __init__(self, parameters:dict) -> None:
        super().__init__()
        self.parameters = parameters

    def __repr__(self) -> str:
        return super().__repr__()
    
class TransferCharacteristicPower(TransferCharacteristicParametric):
    """A power function transfer characteristic"""

    def __init__(self, parameters: dict={"a": 1.0}) -> None:
        super().__init__(parameters)

    @property
    def parameters(self):
        return self._parameters
    
    @parameters.setter
    def parameters(self, value):
        if type(value) is not dict: raise Exception("Parameters must be a dict")
        if len(value) != 1: raise Exception("TransferCharacteristicPower only takes one parameter.")
        self._parameters = value

    def forward_transfer(self, data):
        new_data = []
        for idx, x in enumerate(data):
            new_data.append(pow(x, list(self.parameters.values())[0]))

        return new_data

    def inverse_transfer(self, data):
        new_data = []
        for idx, x in enumerate(data):
            new_data.append(pow(x, 1.0 / list(self.parameters.values())[0]))

        return new_data

    def valid(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "TransferCharacteristicPower(parameters=%r)" % (self.parameters)
    
class TransferCharacteristicPowerWithBreak(TransferCharacteristicParametric):
    """A power function with a linear segment near zero transfer characteristic"""

    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)

    @property
    def parameters(self):
        return self._parameters
    
    @parameters.setter
    def parameters(self, value):
        if type(value) is not dict: raise Exception("TransferCharacteristic parameters must be a dict")
        if len(value) != 5: raise Exception("TransferCharacteristicPowerWithBreak takes only exactly five parameters.")
        self._parameters = value

    def forward_transfer(self, data):
        new_data = []
        for idx, x in enumerate(data):
            item = x
            if(item <= self.parameters["d"]):
                item = self.parameters["c"] * item
            else:
                item = self.parameters["a"] * pow(item, 1.0 / self.parameters["g"]) + self.parameters["b"]
            new_data.append(item)

        return new_data

    def inverse_transfer(self, data):
        new_data = []
        cut_off = self.parameters["c"] * self.parameters["d"]
        for idx, x in enumerate(data):
            item = x
            if(item <= cut_off):
                item =  item / self.parameters["c"]
            else:
                item = pow((item - self.parameters["b"]) / self.parameters["a"], self.parameters["g"])
            new_data.append(item)

        return new_data
    
    def valid(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "TransferCharacteristicPowerWithBreak(parameters=%r)" % (self.parameters)

class TransferCharacteristicLog10WithBreak(TransferCharacteristicParametric):
    """A log10 function with a linear section near zero"""

    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        if type(value) is not dict: raise Exception("TransferCharacteristic parameters must be a dict")
        if len(value) != 7: raise Exception("TransferCharacteristicPowerWithBreak takes only exactly seven parameters.")
        self._parameters = value

    def forward_transfer(self, data):
        new_data = []
        a = self.parameters["a"]
        b = self.parameters["b"]
        c = self.parameters["c"]
        d = self.parameters["d"]
        e = self.parameters["e"]
        f = self.parameters["f"]
        h = self.parameters["h"]
        for idx, x in enumerate(data):
            item = x
            if(item <= h):
                item = e * item + f
            else:
                item = c * log10(a * item + b) + d
            new_data.append(item)

        return new_data

    def inverse_transfer(self, data):
        new_data = []
        a = self.parameters["a"]
        b = self.parameters["b"]
        c = self.parameters["c"]
        d = self.parameters["d"]
        e = self.parameters["e"]
        f = self.parameters["f"]
        h = self.parameters["h"]

        cut = e * h + f

        for idx, x in enumerate(data):
            item = x
            if(item <= cut):
                item = (item - f) / e
            else:
                item = (pow(10, (item - d) / c) - b) / a
            new_data.append(item)

        return new_data

    def valid(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "TransferCharacteristicLog10WithBreak(parameters=%r)" % (self.parameters)

class TransferCharacteristicSequence(TransferCharacteristic):
    """A transfer function made from a sequence of other transfer functions
        Holds an ordered list of pairs of transfer characteristics and directions
        (either forward or inverse)
    """

    def __init__(self, sequence:list) -> None:
        self.sequence = sequence

    def forward_transfer(self):
        return self.sequence

    def inverse_transfer(self):
        sequence_copy = self.sequence.copy()
        sequence_copy.reverse()
        return sequence_copy

    def valid(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "TransferCharacteristicPower(sequence=%r)" % (self.sequence)

class TransferCharacteristicURI(TransferCharacteristic):
    """A transfer characteristic that references an external file"""

    def __init__(self, URI) -> None:
        self.URI = URI

    def forward_transfer(self, data):
        print("ERROR: You didn't think I'd written my own LUT engine yet did you?")

    def inverse_transfer(self,data):
        print("ERROR: You didn't think I'd written my own LUT engine yet did you?")

    def valid(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "TransferCharacteristicURI(URI=%r)" % (self.URI)