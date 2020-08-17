import unittest
from mock import MagicMock, patch
from werkzeug.exceptions import NotFound
from ....webapp.lib.company_resources import (
    get_employees_from_company_resources, get_employee_from_response)
from ....webapp.errors_handler import ExternalUrlError


class TestCompanyResources(unittest.TestCase):
    @patch("requests.get")
    def test_get_employees_from_company_resources(self, requests_mock):
        get_employees_from_company_resources(MagicMock())
        requests_mock.assert_called_once()

    def test_get_employee_from_response_with_empty_response_raises_error(self):
        self.assertRaises(
            NotFound, get_employee_from_response, [], MagicMock())

    def test_get_employee_from_response_with_bigger_than_one_len_response_raises_error(self):
        self.assertRaises(
            NotFound, get_employee_from_response, [MagicMock(), MagicMock()], MagicMock())

    def test_get_employee_from_response_with_different_id_raises_error(self):
        identifier_mock = "123"
        other_identifier_mock = "234"
        response_mock = [{"id": identifier_mock}]
        self.assertRaises(
            ExternalUrlError, get_employee_from_response, response_mock, other_identifier_mock)

    def test_get_employee_from_response_with_equal_id_works(self):
        identifier_mock = "123"
        response_mock = [{"id": identifier_mock}]
        self.assertEqual(response_mock[0], get_employee_from_response(
            response_mock, identifier_mock))
