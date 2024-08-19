import allure
import pytest
import requests

from src.constants.api_constants import APIConstants
from src.helpers.api_requests_wrapper import *
from src.helpers.common_verification import *
from src.helpers.payload_manager import payload_create_booking, payload_update_booking
from src.utils.utils import Utils


class TestUpdateDeletedBooking(object):

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
        data = response.json()
        booking_id = data["bookingid"]
        print(f"Created Booking ID: {booking_id}")
        return booking_id

    @allure.title("#TC6 - Trying to update a deleted booking ID")
    @pytest.mark.integration
    def test_update_deleted_booking(self, create_token, create_booking):
        booking_id = create_booking

        # URL for the DELETE request
        delete_url = APIConstants().url_patch_put_delete(booking_id=booking_id)

        # Delete the booking
        delete_response = delete_requests(
            url=delete_url,
            headers=Utils().common_header_put_delete_patch_cookie(token=create_token),
            auth=None,
            in_json=False
        )

        verify_http_status_code(response_data=delete_response, expect_data=201)
        print(f"Deleted Booking ID: {booking_id}")

        # URL for the PATCH request
        update_url = APIConstants().url_patch_put_delete(booking_id=booking_id)


        update_response = patch_requests(
            url=update_url,
            headers=Utils().common_header_put_delete_patch_cookie(token=create_token),
            auth=None,
            payload=payload_update_booking(),
            in_json=False
        )
        verify_http_status_code(response_data=update_response, expect_data=405)
        assert "text/plain" in update_response.headers["Content-Type"]
        print(f"Update Response Status Code: {update_response.status_code}")
        print(f"Update Response Body: {update_response.text}")
