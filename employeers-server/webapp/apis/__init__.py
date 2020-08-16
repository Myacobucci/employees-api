from flask_restx import Api

from .employeers import api as employeers_namespace

api = Api(
    title='Employeers API',
    version='1.0',
    description='This is the API for the employeers project',
)

api.add_namespace(employeers_namespace, '/employeers')
