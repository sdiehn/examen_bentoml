# JWT Authentication Test:

# Verify that authentication fails if the JWT token is missing or invalid.
# Verify that authentication fails if the JWT token has expired.
# Verify that authentication succeeds with a valid JWT token.

import os
import requests
import jwt
from datetime import datetime, timedelta

LOGIN_URL = "http://127.0.0.1:3000/login"
PREDICT_URL = "http://127.0.0.1:3000/predict"


CREDENTIALS={
    "username": "user123",
    "password": "password123"
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


def test_login(username, password, expected_status):
    r=requests.post(LOGIN_URL, json={"credentials": CREDENTIALS})
    token = None
    if r.status_code == 200:
        token = r.json().get("token")
    return token


def test_jwt_auth(valid_token):
    # missing token
    r=requests.post(PREDICT_URL, json=VALID_INPUT)
    print_output("N/A", 401, r.status_code, "Missing Token")
    
    # expired token
    expired_payload = {
        "sub": "user123",
        "exp": datetime.utcnow() - timedelta(hours=1) 
    }
    expired_token = jwt.encode(expired_payload, "your_jwt_secret_key_here", algorithm="HS256")
    r=requests.post(PREDICT_URL, json=VALID_INPUT, headers={"Authorization": f"Bearer {expired_token}"})
    print_output(expired_token, 401, r.status_code, "Expired Token")
  
    # invalid token
    invalid_token = valid_token + "invalid"
    r=requests.post(PREDICT_URL, json=VALID_INPUT, headers={"Authorization": f"Bearer {invalid_token}"})
    print_output(invalid_token, 401, r.status_code, "Invalid Token")
    
    # valid token
    r=requests.post(PREDICT_URL, json=VALID_INPUT, headers={"Authorization": f"Bearer {valid_token}"})
    print_output(valid_token, 200, r.status_code, "Valid Token")


def print_output(token, expected_status, status_code, test_type):
    output = f"""
============================
  {test_type} Test
============================
| Token: {token}
| Expected Status: {expected_status}
| Actual Status: {status_code}
| Result: {"SUCCESS" if status_code == expected_status else "FAILURE"}
"""
    print(output)

if __name__ == "__main__":
    valid_token = test_login("user123", "password123", 200)
    if valid_token:
        test_jwt_auth(valid_token)
    else:
        print("Login failed; cannot perform JWT authentication tests.")
        