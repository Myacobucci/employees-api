from flask_restx import Namespace, Resource, fields
from webargs.flaskparser import use_kwargs
from werkzeug.exceptions import NotFound
from ..utils import (get_json_from_file_resource, get_dict_of_elements_from_json_file_list,
                     validate_id, PAGINATION_ARGUMENTS, DOC_PAGINATION_ARGUMENTS)

api = Namespace('departments', description='Departments')

department_model = api.model('Departments', {
    'id': fields.Integer(required=True, description='The department identifier'),
    'name': fields.String(description='The department name'),
    'superdepartment': fields.Integer(description='The department superdepartment identifier'),
})

DEPARTMENTS_FILENAME = "departments"
DEPARTMENT_ID_KEY = "id"


@api.route('')
class Departments(Resource):
    @api.doc('list_departments', params=DOC_PAGINATION_ARGUMENTS)
    @api.marshal_list_with(department_model)
    @use_kwargs(PAGINATION_ARGUMENTS, location="query")
    def get(self, limit, offset):
        departments = get_json_from_file_resource(DEPARTMENTS_FILENAME)
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
            DEPARTMENTS_FILENAME, DEPARTMENT_ID_KEY)
        department = departments.get(int(identifier))
        if not department:
            raise NotFound("Department not found")

        return department
