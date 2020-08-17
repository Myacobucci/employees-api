from flask_restx import Namespace, Resource, fields
from webargs.flaskparser import use_kwargs
from ..utils import (validate_id, PAGINATION_ARGUMENTS,
                     DOC_PAGINATION_ARGUMENTS)
from ..relationships import (validate_expand_parameter,
                             apply_expand_relationships, EXPAND_ARGUMENT, DOC_EXPAND_ARGUMENT)
from ..lib.company_resources import get_employees_from_company_resources, get_employee_from_response

api = Namespace('employees', description='Employees')

EMPLOYEE_RESOURCE_KEY = "employee"
employee_model = api.model('Employee', {
    'id': fields.Integer(required=True, description='The employee identifier'),
    'first': fields.String(description='The employee first name'),
    'last': fields.String(description='The employee last name'),
    "manager": fields.Raw(description='The employee manager'),
    "department": fields.Raw(description='The employee department'),
    "office": fields.Raw(description='The employee office'),
})


@api.route('')
class Employees(Resource):
    @api.doc('list_employees', params={**DOC_PAGINATION_ARGUMENTS, **DOC_EXPAND_ARGUMENT})
    @api.marshal_list_with(employee_model)
    @use_kwargs({**PAGINATION_ARGUMENTS, **EXPAND_ARGUMENT}, location="query")
    def get(self, limit, offset, expand):
        validate_expand_parameter(expand, EMPLOYEE_RESOURCE_KEY)

        params = {"limit": limit, "offset": offset}
        employees = get_employees_from_company_resources(params)
        apply_expand_relationships(expand, employees)

        return employees


@api.route('/<identifier>')
@api.param('identifier', 'The employeer identifier')
@api.response(404, 'Employeer not found')
class Employeer(Resource):
    @api.doc('get_employeer', params=DOC_EXPAND_ARGUMENT)
    @api.marshal_with(employee_model)
    @use_kwargs(EXPAND_ARGUMENT, location="query")
    def get(self, identifier, expand):
        validate_id(identifier)
        validate_expand_parameter(expand, EMPLOYEE_RESOURCE_KEY)

        params = {"id": identifier}
        response = get_employees_from_company_resources(params)
        apply_expand_relationships(expand, response)
        employee = get_employee_from_response(response, identifier)

        return employee
