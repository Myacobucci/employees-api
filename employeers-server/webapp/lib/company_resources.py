import requests
from werkzeug.exceptions import NotFound
from ..errors_handler import ExternalUrlError
from ...settings import COMPANY_RESOURCES_URL


COMPANY_RESOURCES_URL_TIMEOUT = 30
EMPLOYEES_PATH = "/employees"


def get_employees_from_company_resources(params):
    response = requests.get(
        f"{COMPANY_RESOURCES_URL}{EMPLOYEES_PATH}", params=params, timeout=COMPANY_RESOURCES_URL_TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_employee_from_response(response, identifier):
    if response and len(response) == 1:
        employee = response[0]
        if str(employee["id"]) != identifier:
            raise ExternalUrlError(
                "The response from the external employees URL was not the "
                "expected one (different identifier).")
        return employee
    raise NotFound("Employee not found")
