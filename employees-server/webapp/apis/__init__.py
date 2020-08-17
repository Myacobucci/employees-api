from flask_restx import Api
from .employees import api as employees_namespace
from .offices import api as offices_namespace
from .departments import api as departments_namespace
from ..errors_handler import configure_error_handling

api = Api(
    title='Employees API',
    version='1.0',
    description='This is the API for the employees project',
)
configure_error_handling(api)

api.add_namespace(employees_namespace, '/employees')
api.add_namespace(offices_namespace, '/offices')
api.add_namespace(departments_namespace, '/departments')
