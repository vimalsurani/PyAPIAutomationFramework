import allure
import pytest
import requests

from src.constants.api_constants import APIConstants
from src.helpers.api_requests_wrapper import *
from src.helpers.common_verification import *
from src.helpers.payload_manager import payload_invalid
from src.utils.utils import Utils


class TestInvalidCreation(object):

    @allure.title("#TC5 - Invalid creation with wrong payload or wrong JSON")
    @pytest.mark.integration
    def test_invalid_creation(self):
        URL = APIConstants().url_create_booking()
        headers = Utils().common_headers_json()

        # Sending POST request with invalid payload
        response = post_request(
            url=URL,
            headers=headers,
            auth=None,
            payload=payload_invalid(),
            in_json=False
        )

        # Verify response status code is not 200 (expected failure)
        verify_http_status_code(response_data=response,
                                expect_data=500)  # 400 Bad Request is a common response for invalid payloads

        # Output response details
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

