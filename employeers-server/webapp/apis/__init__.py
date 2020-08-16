from flask_restx import Api
from .employeers import api as employeers_namespace
from ..errors_handler import configure_error_handling

api = Api(
    title='Employeers API',
    version='1.0',
    description='This is the API for the employeers project',
)
configure_error_handling(api)

api.add_namespace(employeers_namespace, '/employeers')
