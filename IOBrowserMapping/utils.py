import os
import re
import pandas as pd


def read_data(filename):
    extension = os.path.splitext(filename)[1]
    if extension == '.csv':
        data = pd.read_csv(filename, delimiter=';', header=None)
    else:
        data = pd.read_excel(filename, header=None)

    processed_data = pd.DataFrame(
        list(data.apply(transform_line_to_four_columns, axis=1)),
        columns=None,
        index=None
    )
    return processed_data

def get_direction(address):
    if address.startswith("%Q"):
        return "ReadFromPLC"
    if address.startswith("%I"):
        return "WriteToPLC"
    if address.startswith("%M"):
        return "Bidirectional"

def transform_line_to_four_columns(value):
    # Extraire les valeurs du module, numéro, et identifiant

    pattern = r"(?P<module>[A-Z]+)(?P<number>\d+)\.(?P<identifier>[A-Za-z_\.]*)\.(?P<value>[A-Za-z_]*)"
    # pattern = r"(?P<module>[A-Z])(?P<number>\d{3})?\.(?P<identifier>[A-Za-z_\.]*)\.(?P<direction>[A-Za-z_]+)"
    match = re.search(pattern, value[0])

    if not match:
        # Si le format ne correspond pas, retourner des cellules vides
        return [None, None, None, None]

    module = match.group("module")
    number = match.group("number")
    identifier = match.group("identifier")
    variable = match.group("value")
    _type = value[1]
    type_address = value[2][1:3]

    type_address, number_address = (type_address[0], value[2][2:]) if type_address[1].isdigit() else (
    type_address, value[2][3:])
    direction = get_direction(value[2])
    return [module, number, identifier, variable, _type, type_address, number_address, direction]

