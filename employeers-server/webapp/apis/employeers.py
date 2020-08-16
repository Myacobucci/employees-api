from flask_restx import Namespace, Resource, fields
from webargs.flaskparser import use_kwargs
from .utils import PAGINATION_ARGUMENTS, DOC_PAGINATION_ARGUMENTS, validate_id
from ..lib.company_resources import get_employees_from_company_resources, get_employee_from_response

api = Namespace('employeers', description='Employeers')

employee_model = api.model('Employeer', {
    'id': fields.Integer(required=True, description='The employee identifier'),
    'first': fields.String(description='The employee first name'),
    'last': fields.String(description='The employee last name'),
    'manager': fields.Integer(description='The employee manager'),
    'department': fields.Integer(description='The employee department'),
    'office': fields.Integer(description='The employee office'),
})


@api.route('')
class Employeers(Resource):
    @api.doc('list_employeers', params=DOC_PAGINATION_ARGUMENTS)
    @api.marshal_list_with(employee_model)
    @use_kwargs(PAGINATION_ARGUMENTS, location="query")
    def get(self, limit, offset):
        params = {"limit": limit, "offset": offset}
        return get_employees_from_company_resources(params)


@api.route('/<identifier>')
@api.param('identifier', 'The employeer identifier')
@api.response(404, 'Employeer not found')
class Employeer(Resource):
    @api.doc('get_employeer')
    @api.marshal_with(employee_model)
    def get(self, identifier):
        validate_id(identifier)

        params = {"id": identifier}
        response = get_employees_from_company_resources(params)
        employee = get_employee_from_response(response, identifier)

        return employee
