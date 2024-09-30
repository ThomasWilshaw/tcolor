import yaml
from . import Colourimetry
from . import TransferCharacteristic
import uritools

class TColor():
    """Contains a set of known colour spaces. Allows for interacting with and 
    adding or removing colour spaces"""

    def __init__(self) -> None:
        self.config = {}

    def RGBPrimaries_from_YAML(self, yaml_input) -> Colourimetry.RGBPrimaries:
        try:
            red = yaml_input["Red"]
            green = yaml_input["Green"]
            blue = yaml_input["Blue"]

            primaries = Colourimetry.RGBPrimaries(list(red.values()), list(green.values()), list(blue.values()))

            return primaries
        except KeyError as e:
            print("YAML ERROR: ", e)

    def achromatic_centroid_from_YAML(self, yaml_input):
        try:
            return [yaml_input["x"], yaml_input["y"]]
        except KeyError as e:
            print("YAML ERROR: ", e)

    def transfer_charactersitc_from_YAML(self, yaml_input):
        try:
            tc_type = yaml_input[0]["Type"]
            
            if tc_type == "Parametric":
                function = yaml_input[1]["Function"]
                if function == "powerwithbreak":
                    return TransferCharacteristic.TransferCharacteristicPowerWithBreak(yaml_input[2]["Parameters"])
                elif function == "power":
                    return TransferCharacteristic.TransferCharacteristicPower(yaml_input[2]["Parameters"])
                elif function == "log10withbreak":
                    return TransferCharacteristic.TransferCharacteristicLog10WithBreak(yaml_input[2]["Parameters"])
                else:
                    raise ValueError("Transfer Characteristic function not supported", function)

            elif tc_type == "Sequence":
                return TransferCharacteristic.TransferCharacteristicSequence(yaml_input[1]["Sequence"])

            elif tc_type == "URI":
                if uritools.isuri(yaml_input[1]["URI"]):
                    return TransferCharacteristic.TransferCharacteristicURI(yaml_input[1]["URI"])
                else:
                    raise ValueError("YAML ERROR, invalid URI: ", yaml_input)

            else:
               raise ValueError("YAML ERROR, invald Transfer Characteristic type: ", yaml_input)
            
        except KeyError as e:
            print("YAML ERROR: ", e)

    def colourimetry_from_YAML(self,name, yaml_colourimetry):
        new_colourimetry_set = Colourimetry.Colourimetry()
        new_colourimetry_set.descriptor = name

        if "RGB Primaries" in yaml_colourimetry:
            primaries = yaml_colourimetry["RGB Primaries"]
            if type(primaries) is dict:
                new_colourimetry_set.primaries = self.RGBPrimaries_from_YAML(primaries)
            elif type(primaries) is str:
                new_colourimetry_set.primaries = Colourimetry.RGBPrimaries(reference=primaries)
            else:
                new_colourimetry_set.primaries = primaries

        if "Achromatic Centroid" in yaml_colourimetry:
            achromatic_centroid = yaml_colourimetry["Achromatic Centroid"]
            if type(achromatic_centroid) is dict:
                new_colourimetry_set.achromatic = self.achromatic_centroid_from_YAML(achromatic_centroid)
            else:
                new_colourimetry_set.achromatic = achromatic_centroid

        if "Transfer Characteristic" in yaml_colourimetry:
            transfer_characteristic = yaml_colourimetry["Transfer Characteristic"]
            if type(transfer_characteristic) is list:
                new_colourimetry_set.transfer_characteristic = self.transfer_charactersitc_from_YAML(transfer_characteristic)
            else:
                new_colourimetry_set.transfer_characteristic = TransferCharacteristic.TransferCharacteristic()

        if "Hints" in yaml_colourimetry:
            new_colourimetry_set.hints = yaml_colourimetry["Hints"]

        if "Alias" in yaml_colourimetry:
            new_colourimetry_set.alias = yaml_colourimetry["Alias"]

        if "CIE Version" in yaml_colourimetry:
            new_colourimetry_set.cie_version = yaml_colourimetry["CIE Version"]

        return new_colourimetry_set

    def parse_data(self, data:list):
        """Parse the YAML data"""
        for id, idx in enumerate(data):
 
            name = list(data[id].keys())[0]
            yaml_colourimetry = data[id][name]

            if name in self.config:
                print("WARNING: Colour space repeated (" + name + ")")
                print("Only Alias and Hints can be merged. To redifine colourimetry lease delete the chunk and re add")
                new_colourimetry = self.colourimetry_from_YAML(name, yaml_colourimetry)
                existing_colourimetry = self.config[name]

                #print(existing_colourimetry)

                existing_colourimetry.hints = existing_colourimetry.hints + new_colourimetry.hints
                existing_colourimetry.alias = existing_colourimetry.alias + new_colourimetry.alias
            else:
                try:
                    self.config[str(name)] = self.colourimetry_from_YAML(name, yaml_colourimetry)
                except Exception as e:
                    print(e, "Skipping this Colourimetry chunk")

    def update_references(self):
        """Loop through the config and update any references"""

        for key, value in self.config.items():
            value:Colourimetry
            # TODO: Make recursive maybe?
            if not value.primaries.valid():
                if value.primaries.reference:
                    self.config[key].primaries = self.config[value.primaries.reference].primaries

            if not value.achromatic_valid():
                if type(value.achromatic) is str:
                    self.config[key].achromatic = self.config[value.achromatic].achromatic

            if not value.transfer_characteristic.valid():
                pass
                #print(key)
                

    def add_colour_space(self, colour_space):
        """Add a colour space to the config as either a file or a string"""

        with open(colour_space, 'r') as file:
            data = yaml.safe_load(file)
            self.parse_data(data)
            self.update_references()

    def print_colourimetry(self, descriptor):
        """Pretty prints the colourimetry data set for the given descriptor"""

        item:Colourimetry = self.config[descriptor]
        print("-", item.descriptor)
        print("\tRGB Primaries: " + item.primaries.__str__())
        print("\tAchromatic Centroid: ", item.achromatic)
        print("\tTransfer Characteristic:",  item.transfer_characteristic)
        print("\tHints: ", item.hints)
        print("\tAlias: ", item.alias)
        print("\tCIE Version:", item.cie_version)
        print()

    def print_all_colourimetry(self):
        for key, value in self.config.items():
            self.print_colourimetry(key)
            


if __name__ == "__main__":
    config = TColor()

    config.add_colour_space("..\\tests\\files\\tcolor_test.yaml")
    config.print_all_colourimetry()
