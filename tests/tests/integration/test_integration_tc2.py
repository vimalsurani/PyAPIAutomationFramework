import allure
import pytest
import logging

from src.constants.api_constants import APIConstants
from src.helpers.api_requests_wrapper import *
from src.helpers.common_verification import *
from src.helpers.payload_manager import *
from src.utils.utils import Utils


class TestDeleteBooking(object):

    @pytest.fixture()
    def create_booking(self):
        print("Create Booking ID")
        response = post_request(
            url=APIConstants().url_create_booking(),
            headers=Utils().common_headers_json(),
            auth=None,
            payload=payload_create_booking(),
            in_json=False
        )
        verify_http_status_code(response_data=response, expect_data=200)
        booking_id = response.json()["bookingid"]
        # logging.info(f"Created Booking ID: {booking_id}")
        print(f"Created Booking ID: {booking_id}")
        return booking_id

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
        token = response.json()["token"]
        verify_json_key_for_not_null_token(token)
        return token

    @allure.title("#TC2 - Delete the booking and Verify that it should not exist")
    @pytest.mark.integration
    def test_create_and_delete_booking(self, create_booking, create_token):
        booking_id = create_booking
        token = create_token

        # Delete the booking
        delete_url = APIConstants().url_patch_put_delete(booking_id=booking_id)
        headers = Utils().common_header_put_delete_patch_cookie(token=token)

        delete_response = delete_requests(
            url=delete_url,
            headers=headers,
            auth=None,
            in_json=False
        )
        verify_http_status_code(response_data=delete_response, expect_data=201)
        # logging.info(f"Deleted Booking ID: {booking_id}")
        print(f"Deleted Booking ID: {booking_id}")

        # Verify booking should not exist after deletion
        get_response = get_request(url=delete_url, auth=None)
        verify_http_status_code(response_data=get_response, expect_data=404)
        # logging.info(f"Verified Booking ID {booking_id} does not exist")
        print(f"Verified Booking ID {booking_id} does not exist")
