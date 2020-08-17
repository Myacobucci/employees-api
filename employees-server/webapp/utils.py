import os
import json
from functools import lru_cache
from webargs import validate, fields as webargs_fields
from .errors_handler import ParametersError

PAGINATION_ARGUMENTS = {
    "limit": webargs_fields.Int(missing=100, validate=[validate.Range(min=0, max=1000)]),
    "offset": webargs_fields.Int(missing=0, validate=[validate.Range(min=0)]),
}

DOC_PAGINATION_ARGUMENTS = {
    "limit": {"description": "Number of results. Max value: 1000.", "default": 100, "type": "integer"},
    "offset": {"description": "Offset", "default": 0, "type": "integer"},
}
DEPARTMENTS_FILENAME = "departments"
OFFICES_FILENAME = "offices"

def validate_id(identifier):
    if not identifier.isdigit():
        raise ParametersError(
            "Id should be an integer greater or equal than 0")


@lru_cache(maxsize=1)
def get_json_from_file_resource(filename):
    file_path = f"../resources/{filename}.json"
    filename = os.path.join(os.path.dirname(__file__), file_path)
    with open(filename, 'r') as json_data:
        json_data = json.load(json_data)
        return json_data


@lru_cache(maxsize=1)
def get_dict_of_elements_from_json_file_list(filename, key):
    list_of_dicts = get_json_from_file_resource(filename)
    return {element[key]: element for element in list_of_dicts}
