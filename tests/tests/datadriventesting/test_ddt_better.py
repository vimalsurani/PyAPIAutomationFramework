# Read the CSV or EXCEL file
# Create a Function create_token which can take values from the Excel File
# Verify the Expected Result.

# Read the Excel - openpyxl
import openpyxl
import pytest

from src.constants.api_constants import APIConstants
from src.helpers.api_requests_wrapper import *
from src.utils.utils import Utils
from tests.tests.datadriventesting.test_ddt import read_credentials_from_excel


def create_auth_request(username, password):
    payload = {
        "username": username,
        "password": password
    }
    response = post_request(
        url=APIConstants().url_create_token(),
        headers=Utils().common_headers_json(),
        auth=None,
        payload=payload,
        in_json=False
    )
    return response


@pytest.mark.parametrize("user_cred", read_credentials_from_excel(
    "C:/Users/ViMS/PycharmProjects/PyAPIAutomationFramework/tests/tests/datadriventesting/testdata_ddt.xlsx"))
def test_create_auth_with_excel(user_cred):
    username = user_cred["username"]
    password = user_cred["password"]
    print(username, password)
    response = create_auth_request(username=username, password=password)
    print(response.status_code)