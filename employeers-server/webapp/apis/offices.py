from flask_restx import Namespace, Resource, fields
from webargs.flaskparser import use_kwargs
from werkzeug.exceptions import NotFound
from ..utils import (get_json_from_file_resource, get_dict_of_elements_from_json_file_list,
                     validate_id, PAGINATION_ARGUMENTS, DOC_PAGINATION_ARGUMENTS)

api = Namespace('offices', description='Offices')

office_model = api.model('Office', {
    'id': fields.Integer(required=True, description='The office identifier'),
    'city': fields.String(description='The office city'),
    'country': fields.String(description='The office country'),
    'address': fields.String(description='The office address'),
})

OFFICES_FILENAME = "offices"
OFFICE_ID_KEY = "id"


@api.route('')
class Offices(Resource):
    @api.doc('list_offices', params=DOC_PAGINATION_ARGUMENTS)
    @api.marshal_list_with(office_model)
    @use_kwargs(PAGINATION_ARGUMENTS, location="query")
    def get(self, limit, offset):
        offices = get_json_from_file_resource(OFFICES_FILENAME)
        return offices[offset: offset + limit]


@api.route('/<identifier>')
@api.param('identifier', 'The office identifier')
@api.response(404, 'Office not found')
class Office(Resource):
    @api.doc('get_office')
    @api.marshal_with(office_model)
    def get(self, identifier):
        validate_id(identifier)

        offices = get_dict_of_elements_from_json_file_list(
            OFFICES_FILENAME, OFFICE_ID_KEY)
        office = offices.get(int(identifier))
        if not office:
            raise NotFound("Office not found")

        return office
