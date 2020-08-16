from flask_restx import Namespace, Resource, fields
from webargs.flaskparser import use_kwargs
from .utils import PAGINATION_ARGUMENTS, DOC_PAGINATION_ARGUMENTS, validate_id
from ..lib.company_resources import get_employees_from_company_resources, get_employee_from_response

api = Namespace('employeers', description='Employeers')

employeer = api.model('Employeer', {
    'id': fields.String(required=True, description='The employeer identifier'),
})


@api.route('')
class Employeers(Resource):
    @api.doc('list_employeers', params=DOC_PAGINATION_ARGUMENTS)
    @api.marshal_list_with(employeer)
    @use_kwargs(PAGINATION_ARGUMENTS, location="query")
    def get(self, limit, offset):
        params = {"limit": limit, "offset": offset}
        return get_employees_from_company_resources(params)


@api.route('/<identifier>')
@api.param('identifier', 'The employeer identifier')
@api.response(404, 'Employeer not found')
class Employeer(Resource):
    @api.doc('get_employeer')
    @api.marshal_with(employeer)
    def get(self, identifier):
        validate_id(identifier)

        params = {"id": identifier}
        response = get_employees_from_company_resources(params)
        employee = get_employee_from_response(response, identifier)

        return employee
