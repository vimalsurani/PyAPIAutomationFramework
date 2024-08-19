from faker import Faker
import json

faker = Faker()


def payload_create_booking():
    payload = {
        "firstname": "Amit",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    return payload


def payload_update_booking():
    payload = {
        "firstname": "Vimal",
    }
    return payload

def payload_update():
    payload = {
            "firstname": "Vimal",
            "lastname": "Patel",
            "totalprice": 200,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2019-01-01",
                "checkout": "2019-12-31"
            },
            "additionalneeds": "Dinner"
    }
    return payload

def payload_invalid():
    payload = {
        "firstname": 456,  # Invalid type
        "lastname": "Brown",
        "totalprice": "one hundred and eleven",  # Invalid type
        "depositpaid": "yes",  # Invalid type
        "bookingdates": {
            "checkin": "45/78/888.5",  # Invalid date format
            "checkout": "45/78/888.5"  # Invalid date format
        },
        "additionalneeds": "Breakfast"
    }
    return payload

def payload_create_booking_dynamic():
    payload = {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=1000),
        "depositpaid": faker.boolean(),
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": faker.random_element(elements=("Breakfast", "Parking", "WiFi", "Extra Bed"))
    }
    return payload


def payload_create_token():
    payload = {
        "username": "admin",
        "password": "password123"
    }
    return payload
