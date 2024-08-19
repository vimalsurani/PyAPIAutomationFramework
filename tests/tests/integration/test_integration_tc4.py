import allure
import pytest
import logging

from src.constants.api_constants import APIConstants
from src.helpers.api_requests_wrapper import *
from src.helpers.common_verification import *
from src.helpers.payload_manager import *
from src.utils.utils import Utils


class TestCreateAndDeleteBooking(object):

    @pytest.fixture()
    @allure.title("Create a new booking")
    def create_booking(self):
        response = post_request(
            url=APIConstants().url_create_booking(),
            headers=Utils().common_headers_json(),
            auth=None,
            payload=payload_create_booking(),
            in_json=False
        )
        verify_http_status_code(response_data=response, expect_data=200)
        verify_json_key_for_not_null(response.json().get("bookingid"))
        booking_id = response.json()["bookingid"]
        # logging.info(f"Created Booking ID: {booking_id}")
        print(f"Created Booking ID: {booking_id}")
        return booking_id

    @allure.title("#TC4 - Create a booking and delete it")
    @pytest.mark.integration
    def test_create_and_delete_booking(self, create_token, create_booking):
        booking_id = create_booking
        delete_url = APIConstants().url_patch_put_delete(booking_id=booking_id)
        headers = Utils().common_header_put_delete_patch_cookie(token=create_token)

        # Delete the booking
        delete_response = delete_requests(
            url=delete_url,
            headers=headers,
            auth=None,
            in_json=False
        )
        verify_http_status_code(response_data=delete_response, expect_data=201)
        # logging.info(f"Deleted Booking ID: {booking_id}")
        print(f"Deleted Booking ID: {booking_id}")

        # Verify that the booking is deleted
        get_response = get_request(url=delete_url, auth=None)
        verify_http_status_code(response_data=get_response, expect_data=404)
        # logging.info(f"Verified deletion of Booking ID: {booking_id}")
        print(f"Verified deletion of Booking ID: {booking_id}")
