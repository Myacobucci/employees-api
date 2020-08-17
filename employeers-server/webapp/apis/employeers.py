from flask_restx import Namespace, Resource, fields
from webargs.flaskparser import use_kwargs
from ..utils import (validate_id, PAGINATION_ARGUMENTS,
                     DOC_PAGINATION_ARGUMENTS)
from ..relationships import (validate_expand_parameter, get_resources_for_expand,
                             apply_expand_relationships, EXPAND_ARGUMENT)
from ..lib.company_resources import get_employees_from_company_resources, get_employee_from_response

api = Namespace('employeers', description='Employeers')

EMPLOYEE_RESOURCE_KEY = "employee"
employee_model = api.model('Employeer', {
    'id': fields.Integer(required=True, description='The employee identifier'),
    'first': fields.String(description='The employee first name'),
    'last': fields.String(description='The employee last name'),
    "manager": fields.Raw(description='The employee manager'),
    "department": fields.Raw(description='The employee department'),
    "office": fields.Raw(description='The employee office'),
})


@api.route('')
class Employeers(Resource):
    @api.doc('list_employeers', params=DOC_PAGINATION_ARGUMENTS)
    @api.marshal_list_with(employee_model)
    @use_kwargs({**PAGINATION_ARGUMENTS, **EXPAND_ARGUMENT}, location="query")
    def get(self, limit, offset, expand):
        validate_expand_parameter(expand, EMPLOYEE_RESOURCE_KEY)

        params = {"limit": limit, "offset": offset}
        employees = get_employees_from_company_resources(params)

        employees_resources_for_expand = get_resources_for_expand(
            expand, employees)
        apply_expand_relationships(
            expand, employees, employees_resources_for_expand)
        return employees


@api.route('/<identifier>')
@api.param('identifier', 'The employeer identifier')
@api.response(404, 'Employeer not found')
class Employeer(Resource):
    @api.doc('get_employeer')
    @api.marshal_with(employee_model)
    @use_kwargs(EXPAND_ARGUMENT, location="query")
    def get(self, identifier, expand):
        validate_id(identifier)
        validate_expand_parameter(expand, EMPLOYEE_RESOURCE_KEY)

        params = {"id": identifier}
        response = get_employees_from_company_resources(params)
        employees_resources_for_expand = get_resources_for_expand(
            expand, response)
        apply_expand_relationships(
            expand, response, employees_resources_for_expand)
        employee = get_employee_from_response(response, identifier)

        return employee
