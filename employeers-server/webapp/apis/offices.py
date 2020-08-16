from flask_restx import Namespace, Resource, fields
from webargs.flaskparser import use_kwargs
from .utils import PAGINATION_ARGUMENTS, DOC_PAGINATION_ARGUMENTS, get_json_from_file_resource

api = Namespace('offices', description='Offices')

office_model = api.model('Office', {
    'id': fields.Integer(required=True, description='The office identifier'),
    'city': fields.String(description='The office city'),
    'country': fields.String(description='The office country'),
    'address': fields.String(description='The office address'),
})

OFFICES_FILENAME = "offices"


@api.route('')
class Offices(Resource):
    @api.doc('list_offices', params=DOC_PAGINATION_ARGUMENTS)
    @api.marshal_list_with(office_model)
    @use_kwargs(PAGINATION_ARGUMENTS, location="query")
    def get(self, limit, offset):
        offices = get_json_from_file_resource(OFFICES_FILENAME)
        return offices[offset: offset + limit]
