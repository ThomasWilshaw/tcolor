import yaml
from . import colourimetry
from . import transfer_characteristic as tc
import uritools

class Config():
    """Contains a set of colourimetry chunks. Allows for interacting with and 
    adding or removing colourimetry chunks"""

    def __init__(self) -> None:
        self.config = {}

    def RGBPrimaries_from_YAML(self, yaml_input) -> colourimetry.RGBPrimaries:
        try:
            red = yaml_input["Red"]
            green = yaml_input["Green"]
            blue = yaml_input["Blue"]

            primaries = colourimetry.RGBPrimaries(list(red.values()), list(green.values()), list(blue.values()))

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
                    return tc.TransferCharacteristicPowerWithBreak(yaml_input[2]["Parameters"])
                elif function == "power":
                    return tc.TransferCharacteristicPower(yaml_input[2]["Parameters"])
                elif function == "log10withbreak":
                    return tc.TransferCharacteristicLog10WithBreak(yaml_input[2]["Parameters"])
                else:
                    raise ValueError("Transfer Characteristic function not supported", function)

            elif tc_type == "Sequence":
                return tc.TransferCharacteristicSequence(yaml_input[1]["Sequence"])

            elif tc_type == "URI":
                if uritools.isuri(yaml_input[1]["URI"]):
                    return tc.TransferCharacteristicURI(yaml_input[1]["URI"])
                else:
                    raise ValueError("YAML ERROR, invalid URI: ", yaml_input)

            else:
               raise ValueError("YAML ERROR, invald Transfer Characteristic type: ", yaml_input)
            
        except KeyError as e:
            print("YAML ERROR: ", e)

    def colourimetry_from_YAML(self,name, yaml_colourimetry):
        new_colourimetry_set = colourimetry.Colourimetry()
        new_colourimetry_set.descriptor = name

        if "RGB Primaries" in yaml_colourimetry:
            primaries = yaml_colourimetry["RGB Primaries"]
            if type(primaries) is dict:
                new_colourimetry_set.primaries = self.RGBPrimaries_from_YAML(primaries)
            elif type(primaries) is str:
                new_colourimetry_set.primaries = colourimetry.RGBPrimaries(reference=primaries)
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
                new_colourimetry_set.transfer_characteristic = tc.TransferCharacteristic()

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
                print("WARNING: Colour imetry chunk repeated (" + name + "). Will attempt merge")
                print("Only Alias and Hints can be merged. To redifine colourimetry please delete the chunk and re add")
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
            # TODO: Make recursive maybe?
            if not value.primaries.valid():
                if value.primaries.reference:
                    self.config[key].primaries = self.get_colourimetry(value.primaries.reference).primaries

            if not value.achromatic_valid():
                if type(value.achromatic) is str:
                    self.config[key].achromatic = self.get_colourimetry(value.achromatic).achromatic

            if not value.transfer_characteristic.valid():
                pass
                #print(key)
                

    def add_colourimetry(self, input):
        """Add a colourinemtry data to the config as either a file or a string"""

        if isinstance(input, str):
            data = None
            try:
                with open(input, 'r') as file:
                    data = yaml.safe_load(file)
            except Exception:
                try:
                    data = yaml.safe_load(input)
                except Exception as e:
                    print(e, "Could not parse input")

            self.parse_data(data)
            self.update_references()

        elif isinstance(input, colourimetry.Colourimetry):
            if input.descriptor in self.config:
                existing_colourimetry = self.config[input.descriptor]
                existing_colourimetry.hints = existing_colourimetry.hints + input.hints
                existing_colourimetry.alias = existing_colourimetry.alias + input.alias
            else:
                self.config[input.descriptor] = input
        else:
            raise TypeError("Input Colourimetry is of the wrong type. Must be file path, Colourimetry() class or stream")

    def print_colourimetry(self, descriptor):
        """Pretty prints the colourimetry data set for the given descriptor or alias"""

        item:colourimetry = self.get_colourimetry(descriptor)
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

    def get_colourimetry(self, descriptor:str) -> colourimetry:
        try:
            return self.config[descriptor]
        except KeyError:
            for key, value in self.config.items():
                if descriptor in value.alias:
                    return self.config[key]
            raise KeyError("%r not in config" % (descriptor))
            


if __name__ == "__main__":
    config = Config()

    config.add_colourimetry("..\\tests\\files\\tcolor_test.yaml")
    config.print_all_colourimetry()
