import yaml
import Colourimetry
import TransferCharacteristic

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
                else:
                    raise ValueError("Transfer Characteristic function not supported", function)

            elif tc_type == "Sequence":
                return TransferCharacteristic.TransferCharacteristicSequence(yaml_input[1]["Sequence"])

            elif tc_type == "URI":
                raise ValueError("Transfer Characteristic type URI not yet supported", yaml_input)

            else:
               raise ValueError("YAML ERROR, invald Transfer Characteristic type: ", yaml_input)
            
        except KeyError as e:
            print("YAML ERROR: ", e)


    def parse_data(self, data:list):
        """Parse the YAML data"""
        for id, idx in enumerate(data):
            try:
                new_colourimetry_set = Colourimetry.Colourimetry()
                name = list(data[id].keys())[0]
                colour_space = data[id][name]

                new_colourimetry_set.descriptor = name

                if "RGB Primaries" in colour_space:
                    primaries = colour_space["RGB Primaries"]
                    if type(primaries) is dict:
                        new_colourimetry_set.primaries = self.RGBPrimaries_from_YAML(primaries)
                    else:
                        new_colourimetry_set.primaries = primaries

                if "Achromatic Centroid" in colour_space:
                    achromatic_centroid = colour_space["Achromatic Centroid"]
                    if type(achromatic_centroid) is dict:
                        new_colourimetry_set.achromatic = self.achromatic_centroid_from_YAML(achromatic_centroid)
                    else:
                        new_colourimetry_set.achromatic = achromatic_centroid

                if "Transfer Characteristic" in colour_space:
                    transfer_characteristic = colour_space["Transfer Characteristic"]
                    if type(transfer_characteristic) is list:
                        new_colourimetry_set.transfer_characteristic = self.transfer_charactersitc_from_YAML(transfer_characteristic)
                    else:
                        new_colourimetry_set.transfer_characteristic = transfer_characteristic

                if "Hints" in colour_space:
                    new_colourimetry_set.hints = colour_space["Hints"]

                if "Alias" in colour_space:
                    new_colourimetry_set.alias = colour_space["Alias"]

                if "CIE Version" in colour_space:
                    new_colourimetry_set.cie_version = colour_space["CIE Version"]

                self.config[str(name)] = new_colourimetry_set
            except Exception as e:
                print(e, "Skipping this Colourimetry chunk")
                



    def add_colour_space(self, colour_space):
        """Add a colour space to the config as either a file or a string"""

        with open(colour_space, 'r') as file:
            data = yaml.safe_load(file)
            self.parse_data(data)
            


if __name__ == "__main__":
    config = TColor()

    config.add_colour_space("..\\tests\\files\\tcolor_test.yaml")

    for key, value in config.config.items():
        print(key, value)
        pass