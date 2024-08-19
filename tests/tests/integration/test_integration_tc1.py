# 1. Verify that Create Booking -> Patch Request - Verify that firstName is updated.

import allure
import pytest
import logging
from src.helpers.api_requests_wrapper import post_request, patch_requests, get_request
from src.constants.api_constants import APIConstants
from src.helpers.payload_manager import payload_create_booking, payload_update_booking, payload_create_token
from src.helpers.common_verification import *
from src.utils.utils import Utils

class TestPatchBooking(object):

    @pytest.fixture()
    def create_token(self):
        response = post_request(
            url=APIConstants().url_create_token(),
            headers=Utils().common_headers_json(),
            auth=None,
            payload=payload_create_token(),
            in_json=False
        )
        verify_http_status_code(response_data=response, expect_data=200)
        verify_json_key_for_not_null_token(response.json()["token"])
        return response.json()["token"]

    @pytest.fixture()
    def create_booking(self):
        response = post_request(
            url=APIConstants().url_create_booking(),
            auth=None,
            headers=Utils().common_headers_json(),
            payload=payload_create_booking(),
            in_json=False
        )
        verify_http_status_code(response_data=response, expect_data=200)
        booking_id = response.json()["bookingid"]
        verify_json_key_for_not_null(booking_id)
        # logging.info(f"Created Booking ID: {booking_id}")
        print(f"Created Booking ID: {booking_id}")
        return booking_id

    @allure.title("#TC1 - Verify that firstName is updated or not")
    @allure.description("Verify that the firstName is updated in the booking using a PATCH request.")
    @pytest.mark.integration
    def test_create_and_patch_booking(self, create_booking, create_token):
        booking_id = create_booking
        token = create_token

        patch_response = patch_requests(
            url=APIConstants().url_patch_put_delete(booking_id=booking_id),
            headers=Utils().common_header_put_delete_patch_cookie(token=token),
            auth=None,
            payload=payload_update_booking(),
            in_json=False
        )
        verify_http_status_code(response_data=patch_response, expect_data=200)
        patched_data = patch_response.json()
        verify_response_key(patched_data["firstname"], "Vimal")
        # logging.info(f"Patched Booking Data: {patched_data}")
        print(f"Patched Booking Data: {patched_data}")

        # Verify the update via a GET request
        get_response = get_request(
            url=APIConstants().url_patch_put_delete(booking_id=booking_id),
            auth=None
        )
        verify_http_status_code(response_data=get_response, expect_data=200)
        get_data = get_response.json()  # Extract the JSON data from the response
        verify_response_key(get_data["firstname"], "Vimal")
        # logging.info(f"Verified Patched Booking Data: {get_data}")
        print(f"Verified Patched Booking Data: {get_data}")