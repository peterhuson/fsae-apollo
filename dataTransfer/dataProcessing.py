from typing import List, Dict, Tuple
from pint import UnitRegistry

units = UnitRegistry()
units.define("fraction = [] = frac")
units.define("percent = 1e-2 frac = pct")


# Maps serial key to value's name, datatype, and the units the value is in when coming in
key_mapping: Dict[str, Tuple[str, type, units.Quantity]] = {
    "l700": ("coolant_temp", float, units.celsius),
    "h700": ("oil_pressure", float, units.pascal),
    "l701": ("battery_voltage", float, units.volt),
    "h701": ("lambda", float, units.fraction),
    "l702": ("rpm", float, units.radian),
    "h702": ("throttle_pos", float, units.fraction),
    "l703": ("wheel_speed_L", float, units.mph),
    "h703": ("wheel_speed_R", float, units.mph),
    "l704": ("acceleration_Y", float, units.meter / (units.second ** 2)),
    "h704": ("acceleration_Z", float, units.meter / (units.second ** 2))
}


def parse_data(raw_data: List[bytes]) -> Dict[str, units.Quantity]:

    parsed_values = {}

    for raw_data_entry in raw_data:
        raw_data_entry = str(raw_data_entry).strip()
        key = raw_data_entry[:4]
        raw_value = raw_data_entry[5:].strip()  # TODO: might have to change to 5:11 here

        try:
            # Lookup value parameters in mapping
            value_name, value_type, value_units = key_mapping[key]

            # Clean value and apply units if there any
            clean_value = value_type(raw_value)
            if value_units is not None:
                clean_value *= value_units

            # Save the value to return it
            parsed_values[value_name] = clean_value
        except KeyError:
            ...  # TODO: implement logging to log this error
        except ValueError:
            ...  # TODO: logging

    return parsed_values
