import requests
from flask_restx import Namespace, Resource, fields
from webargs.flaskparser import use_kwargs
from .utils import PAGINATION_ARGUMENTS
from ...settings import EMPLOYEERS_URL, EMPLOYEERS_URL_TIMEOUT

api = Namespace('employeers', description='Employeers')

employeer = api.model('Employeer', {
    'id': fields.String(required=True, description='The employeer identifier'),
})


@api.route('')
class Employeers(Resource):
    @api.doc('list_employeers')
    @api.marshal_list_with(employeer)
    @use_kwargs(PAGINATION_ARGUMENTS, location="query")
    def get(self, limit, offset):
        params = {"limit": limit, "offset": offset}
        response = requests.get(
            EMPLOYEERS_URL, params=params, timeout=EMPLOYEERS_URL_TIMEOUT)
        response.raise_for_status()
        return response.json()


@api.route('/<id>')
@api.param('id', 'The employeer identifier')
@api.response(404, 'Employeer not found')
class Employeer(Resource):
    @api.doc('get_employeer')
    @api.marshal_with(employeer)
    def get(self, id):
        raise NotImplementedError
