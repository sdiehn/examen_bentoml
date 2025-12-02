import pytest
import requests
import jwt
from datetime import datetime, timedelta

LOGIN_URL = "http://127.0.0.1:3000/login"
PREDICT_URL = "http://127.0.0.1:3000/v1/models/rfclassifierservice/predict"

VALID_INPUT = {
    "GRE Score": 320,
    "TOEFL Score": 110,
    "University Rating": 4,
    "SOP": 5,
    "LOR": 4,
    "CGPA": 9,
    "Research": 1
}

INVALID_INPUT = {
    "GRE Score": "three twenty",
    "TOEFL Score": 110,
    "University Rating": 4,
    "SOP": 5,
    "LOR": 4,
    "CGPA": 9,
    "Research": 1
}

def get_token():
    response = requests.post(
        LOGIN_URL,
        json={"username": "user123", "password": "password123"}
    )
    if response.status_code == 200:
        return response.json()["token"]
    return None

# authentication tests    

def test_jwt_missing_token():
    response = requests.get(PREDICT_URL)
    assert response.status_code == 401

def test_jwt_invalid_token():
    invalid_header = {"Authorization": "Bearer hallohallo123"}
    response = requests.get(PREDICT_URL, headers=invalid_header)
    assert response.status_code == 401


def test_jwt_expired_token():
    token = get_token()
    expired_payload = {
    "sub": "user123",
    "exp": datetime.utcnow() - timedelta(hours=1) 
    }
    expired_token = jwt.encode(expired_payload, "your_jwt_secret_key_here", algorithm="HS256")
    response = requests.get(PREDICT_URL, headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401


def test_jwt_valid_token():
    token = get_token()
    response = requests.get(PREDICT_URL, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


# login API test

def test_login(username, password, expected):
    response = requests.post(
        LOGIN_URL,
        json=CREDENTIALS
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
    assert response.status_code == 401


def test_predict_valid_input():
    token = get_token()
    response = requests.post(
    PREDICT_URL,
    headers={"Authorization": f"Bearer {token}"},
    json=VALID_INPUT
)
    assert response.status_code == 200