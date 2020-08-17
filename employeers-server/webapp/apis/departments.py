from copy import deepcopy
from flask_restx import Namespace, Resource, fields
from webargs.flaskparser import use_kwargs
from werkzeug.exceptions import NotFound
from ..utils import (get_json_from_file_resource, get_dict_of_elements_from_json_file_list,
                     validate_id, PAGINATION_ARGUMENTS, DOC_PAGINATION_ARGUMENTS, DEPARTMENTS_FILENAME)
from ..relationships import (validate_expand_parameter,
                             apply_expand_relationships, EXPAND_ARGUMENT)

api = Namespace('departments', description='Departments')

DEPARTMENT_RESOURCE_KEY = "department"
DEPARTMENT_ID_FIELD_KEY = "id"
department_model = api.model('Departments', {
    DEPARTMENT_ID_FIELD_KEY: fields.Integer(required=True, description='The department identifier'),
    'name': fields.String(description='The department name'),
    "superdepartment": fields.Raw(description='The department superdepartment identifier'),
})


@api.route('')
class Departments(Resource):
    @api.doc('list_departments', params=DOC_PAGINATION_ARGUMENTS)
    @api.marshal_list_with(department_model)
    @use_kwargs({**PAGINATION_ARGUMENTS, **EXPAND_ARGUMENT}, location="query")
    def get(self, limit, offset, expand):
        validate_expand_parameter(expand, DEPARTMENT_RESOURCE_KEY)

        departments = deepcopy(
            get_json_from_file_resource(DEPARTMENTS_FILENAME))
        apply_expand_relationships(expand, departments)

        return departments[offset: offset + limit]


@api.route('/<identifier>')
@api.param('identifier', 'The department identifier')
@api.response(404, 'Department not found')
class Department(Resource):
    @api.doc('get_department')
    @api.marshal_with(department_model)
    def get(self, identifier):
        validate_id(identifier)

        departments = get_dict_of_elements_from_json_file_list(
            DEPARTMENTS_FILENAME, DEPARTMENT_ID_FIELD_KEY)
        department = departments.get(int(identifier))
        if not department:
            raise NotFound("Department not found")

        return department
