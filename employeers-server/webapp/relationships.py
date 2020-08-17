from copy import deepcopy
from webargs import validate, fields as webargs_fields
from .errors_handler import ParametersError
from .lib.company_resources import get_employees_from_company_resources
from .utils import get_dict_of_elements_from_json_file_list, DEPARTMENTS_FILENAME, OFFICES_FILENAME

EMPLOYEE_RESOURCE_KEY = "employee"
DEPARTMENT_RESOURCE_KEY = "department"
OFFICE_RESOURCE_KEY = "office"
OFFICE_FIELD_KEY = "office"
MANAGER_FIELD_KEY = "manager"
DEPARTMENT_FIELD_KEY = "department"
SUPERDEPARTMENT_FIELD_KEY = "superdepartment"

EXPAND_ARGUMENT = {
    "expand": webargs_fields.String(missing="", validate=validate.Length(min=1)),
}
EXPAND_DELIMITER = "."
EXPAND_RELATIONSHIPS = {
    EMPLOYEE_RESOURCE_KEY: [MANAGER_FIELD_KEY, OFFICE_FIELD_KEY, DEPARTMENT_FIELD_KEY],
    DEPARTMENT_RESOURCE_KEY: [SUPERDEPARTMENT_FIELD_KEY]
}
EXPAND_FIELD_TYPE_DICT = {
    MANAGER_FIELD_KEY: EMPLOYEE_RESOURCE_KEY,
    OFFICE_FIELD_KEY: OFFICE_RESOURCE_KEY,
    DEPARTMENT_FIELD_KEY: DEPARTMENT_RESOURCE_KEY,
    SUPERDEPARTMENT_FIELD_KEY: DEPARTMENT_RESOURCE_KEY,
}

FILENAME_DICT = {
    DEPARTMENT_RESOURCE_KEY: DEPARTMENTS_FILENAME,
    OFFICE_RESOURCE_KEY: OFFICES_FILENAME
}


def validate_expand_parameter(expand, resource_type):
    if not expand:
        return
    expand_relationships = expand.split(EXPAND_DELIMITER)
    parent_resource_type = resource_type
    for resource in expand_relationships:
        validate_expand_relationship(parent_resource_type, resource)
        parent_resource_type = EXPAND_FIELD_TYPE_DICT.get(resource, "")


def validate_expand_relationship(parent_resource_type, resource):
    if not resource in EXPAND_RELATIONSHIPS.get(parent_resource_type, []):
        raise ParametersError("Not a valid expand relationship")


def get_resources_for_expand(expand, resources_to_expand):
    if not expand:
        return {}
    expand_resources_dict = {}
    populate_resources_dict(expand, resources_to_expand, expand_resources_dict)
    return expand_resources_dict


def populate_resources_dict(expand, resources_to_expand, resources_dict):
    expand_splitted = expand.split(EXPAND_DELIMITER, 1)
    first_expand_field = expand_splitted[0]
    expand_resource_type = EXPAND_FIELD_TYPE_DICT[first_expand_field]
    if expand_resource_type != EMPLOYEE_RESOURCE_KEY:
        return
    ids_to_expand = get_ids_of_resources_to_expand(
        resources_to_expand, first_expand_field)
    if expand_resource_type == EMPLOYEE_RESOURCE_KEY:
        add_resources_to_dict(ids_to_expand, resources_dict)

    if len(expand_splitted) > 1:
        resources_to_expand = get_resources_from_dict(
            ids_to_expand, resources_dict, expand_resource_type)
        populate_resources_dict(expand_splitted[1],
                                resources_to_expand, resources_dict)


def get_ids_of_resources_to_expand(resources_to_expand, field):
    return [resource[field] for resource in resources_to_expand if resource.get(field)]


def add_resources_to_dict(ids_to_expand, resources_dict):
    ids_not_in_memory = []
    for id_to_expand in ids_to_expand:
        if id_to_expand not in resources_dict and id_to_expand not in ids_not_in_memory:
            ids_not_in_memory.append(id_to_expand)

    if ids_not_in_memory:
        resources = get_employees_from_company_resources(
            {"id": ids_not_in_memory})
        for resource in resources:
            resources_dict[resource["id"]] = resource


def get_resources_from_dict(ids_to_expand, resources_dict, resource_type):
    if resource_type == EMPLOYEE_RESOURCE_KEY:
        return [resources_dict[id] for id in ids_to_expand]


def apply_expand_relationships(expand, resources_list, employees_resources):
    if not expand:
        return
    for resource in resources_list:
        expand_resource(resource, expand, employees_resources)


def expand_resource(resource, expand, employees_resources):
    expand_splitted = expand.split(EXPAND_DELIMITER, 1)
    first_expand_field = expand_splitted[0]
    expand_resource_type = EXPAND_FIELD_TYPE_DICT[first_expand_field]

    child_resource_id = resource[first_expand_field]
    if child_resource_id:
        child_resource = get_resource(
            expand_resource_type, child_resource_id, employees_resources)
        if len(expand_splitted) > 1:
            expand_resource(
                child_resource, expand_splitted[1], employees_resources)
        resource[first_expand_field] = child_resource


def get_resource(resource_type, resource_id, employees_resources):
    if resource_type == EMPLOYEE_RESOURCE_KEY:
        return deepcopy(employees_resources[resource_id])
    else:
        filename = FILENAME_DICT.get(resource_type, "")
        resources = get_dict_of_elements_from_json_file_list(filename, "id")
        return deepcopy(resources.get(resource_id))
