import allure
import pytest
import logging

from src.constants.api_constants import APIConstants
from src.helpers.api_requests_wrapper import *
from src.helpers.common_verification import *
from src.helpers.payload_manager import *
from src.utils.utils import Utils


class TestUpdateBooking(object):

    @pytest.fixture()
    def get_all_booking_ids(self):
        URL = APIConstants().url_create_booking()  # Same URL for listing bookings
        response = get_request(
            url=URL,
            auth=None
        )
        verify_http_status_code(response_data=response, expect_data=200)
        data = response.json()
        booking_id = data[0]['bookingid']
        # logging.info(f"Booking ID: {booking_id}")
        print(f"Booking ID: {booking_id}")
        return booking_id

    @allure.title("#TC3 - Update a booking and verify using GET by ID")
    @pytest.mark.integration
    def test_get_update_and_verify_booking(self, create_token, get_all_booking_ids):
        booking_id = get_all_booking_ids
        update_url = APIConstants().url_patch_put_delete(booking_id=booking_id)
        headers = Utils().common_header_put_delete_patch_cookie(token=create_token)

        # Update the booking
        update_response = put_requests(
            url=update_url,
            headers=headers,
            auth=None,
            payload=payload_update(),
            in_json=False
        )
        verify_http_status_code(response_data=update_response, expect_data=200)
        updated_data = update_response.json()
        # logging.info(f"Updated Booking Data: {updated_data}")
        print(f"Updated Booking Data: {updated_data}")

        # Verify the update using GET request
        get_response = get_request(url=update_url, auth=None)
        verify_http_status_code(response_data=get_response, expect_data=200)
        verified_data = get_response.json()
        # logging.info(f"Verified Booking Data: {verified_data}")
        print(f"Verified Booking Data: {verified_data}")

        # Assertions
        assert updated_data["firstname"] == "Vimal"
        assert updated_data["lastname"] == "Patel"
        assert updated_data["totalprice"] == 200
        assert updated_data["depositpaid"] is False
        assert updated_data["bookingdates"]["checkin"] == "2019-01-01"
        assert updated_data["bookingdates"]["checkout"] == "2019-12-31"
        assert updated_data["additionalneeds"] == "Dinner"
