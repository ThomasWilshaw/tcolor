from enum import Enum

class TransferCharacteristicType(Enum):
    URI = 1
    PARAMETRIC = 2
    NAMED = 3

class ParametricType(Enum):
    POWER = 1
    
class TransferCharacteristic():
    """Defines a Transfer Characteristic, stored as either a URI, a Parametric or a Named function."""

    def __init__(self, type:TransferCharacteristicType) -> None:
        self.type = type

    def forward_transfer(data):
        """Processes data with the given characteristic transfer function in the forwards direction"""
        pass

    def inverse_transfer(data):
        """Processes data with the given characteristic transfer function in the inverse direction"""
        pass

    def __repr__(self) -> str:
        return "TransferCharacteristic(type=%r)" % (self.type)
    
class TransferCharacteristicParametric(TransferCharacteristic):
    """A parametric transfer function."""

    def __init__(self, type: TransferCharacteristicType, function:ParametricType, parameters:dict) -> None:
        super().__init__(type)
        self.function = function
        self.parameters = parameters

    def __repr__(self) -> str:
        return super().__repr__()
    
class TransferCharacteristicPow(TransferCharacteristicParametric):
    """A power function transfer characteristic"""

    def __init__(self, type: TransferCharacteristicType, function=ParametricType.POWER, parameters: dict={"a": 1.0}) -> None:
        super().__init__(type, function, parameters)

    @property
    def parameters(self):
        return self._parameters
    
    @parameters.setter
    def parameters(self, value):
        if type(value) is not dict: raise Exception("Parameters must be a dict")
        if len(value) != 1: raise Exception("TransferCharacteristicPow only takes one parameter.")
        self._parameters = value

    def forward_transfer(self, data):
        new_data = []
        for idx, x in enumerate(data):
            new_data.append(pow(x, self.parameters.keys[0]))

        return new_data

    def inverse_transfer(self, data):
        new_data = []
        for idx, x in enumerate(data):
            new_data.append(pow(x, 1.0 / self.parameters.keys[0]))

        return new_data

    def __repr__(self) -> str:
        return "TransferCharacteristic(type=%r, function=%r, parameters=%r)" % (self.type, self.function, self.parameters)
    
class TransferCharacteristicPowWithBreak(TransferCharacteristicParametric):
    """A power function with a linear segment near zero transfer characteristic"""

    def __init__(self, type: TransferCharacteristicType, function: ParametricType, parameters: dict) -> None:
        super().__init__(type, function, parameters)

    @property
    def parameters(self):
        return self._parameters
    
    @parameters.setter
    def parameters(self, value):
        if type(value) is not dict: raise Exception("TransferCharacteristic parameters must be a dict")
        if len(value) != 5: raise Exception("TransferCharacteristicPowWithBreak only exactly five parameters.")
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
