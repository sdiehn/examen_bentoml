import pytest
import requests
import jwt
from datetime import datetime, timedelta

LOGIN_URL = f"http://127.0.0.1:3000/login"
PREDICT_URL = f"http://127.0.0.1:3000/predict"


CREDENTIALS = {
    "credentials": {
        "username": "user123",
        "password": "password123"
    }
}

VALID_INPUT = {
    "input_data": {
        "GRE Score": 320,
        "TOEFL Score": 110,
        "University Rating": 5,
        "SOP": 4.5,
        "LOR": 4.0,
        "CGPA": 9.0,
        "Research": 1
    }
}

INVALID_INPUT = {
    "input_data": {
        "GRE Score": "fddfd",
        "TOEFL Score": 110,
        "University Rating": 5,
        "SOP": 4.5,
        "LOR": 4.0,
        "CGPA": 9.0,
        "Research": 1
    }
}

def get_token():
    response = requests.post(
        LOGIN_URL,
        json=CREDENTIALS
    )
    if response.status_code == 200:
        return response.json()["token"]
    return None

# authentication tests    

def test_jwt_missing_token():
    response = requests.post(PREDICT_URL, json=VALID_INPUT)
    assert response.status_code == 401

def test_jwt_invalid_token():
    invalid_header = {"Authorization": "Bearer hallohallo123"}
    response = requests.post(PREDICT_URL, headers=invalid_header, json=VALID_INPUT)
    assert response.status_code == 401


def test_jwt_expired_token():
    token = get_token()
    expired_payload = {
    "sub": "user123",
    "exp": datetime.utcnow() - timedelta(hours=1) 
    }
    expired_token = jwt.encode(expired_payload, "your_jwt_secret_key_here", algorithm="HS256")
    response = requests.post(PREDICT_URL, headers={"Authorization": f"Bearer {expired_token}"}, json=VALID_INPUT)
    assert response.status_code == 401


def test_jwt_valid_token():
    token = get_token()
    response = requests.post(PREDICT_URL, headers={"Authorization": f"Bearer {token}"}, json=VALID_INPUT)
    assert response.status_code == 200


# login API test

@pytest.mark.parametrize(
    "credentials,expected",
    [
        ({"credentials": {"username": "user123", "password": "password123"}}, 200),
        ({"credentials": {"username": "userwrong", "password": "passwordwrong"}}, 401),
    ]
)
def test_login(credentials, expected):
    response = requests.post(
        LOGIN_URL,
        json=credentials
    )
    assert response.status_code == expected

# prediction API tests

def test_predict_with_invalid_input():
    token = get_token()
    response = requests.post(
    PREDICT_URL,
    headers={"Authorization": f"Bearer {token}"},
    json=INVALID_INPUT
)
    assert response.status_code == 400


def test_predict_valid_input():
    token = get_token()
    response = requests.post(
    PREDICT_URL,
    headers={"Authorization": f"Bearer {token}"},
    json=VALID_INPUT
)
    assert response.status_code == 200