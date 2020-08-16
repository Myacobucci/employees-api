from flask_restx import Namespace, Resource, fields


api = Namespace('employeers', description='Employeers')

employeer = api.model('Employeer', {
    'id': fields.String(required=True, description='The employeer identifier'),
})


@api.route('/')
class Employeers(Resource):
    @api.doc('list_employeers')
    @api.marshal_list_with(employeer)
    def get(self):
        raise NotImplementedError


@api.route('/<id>')
@api.param('id', 'The employeer identifier')
@api.response(404, 'Employeer not found')
class Employeer(Resource):
    @api.doc('get_employeer')
    @api.marshal_with(employeer)
    def get(self, id):
        raise NotImplementedError
