'''
Verify that the API returns a 401 error if the JWT token is missing or invalid.
Verify that the API returns a valid prediction for correct input data.
Verify that the API returns an error for invalid input data.
''' 
import requests
import os

LOGIN_URL = "http://127.0.0.1:3000/login"
PREDICT_URL = "http://127.0.0.1:3000/predict"

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
    r=requests.post(LOGIN_URL, json={"username": "user123", "password": "password123"})
    token = None
    if r.status_code == 200:
        token = r.json().get("token")
    return token


def test_valid_prediction(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(PREDICT_URL, json={"input_data": VALID_INPUT}, headers=headers)
    print_output("Valid Prediction", 200, r.status_code)
    

def test_invalid_input(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(PREDICT_URL, json={"input_data": INVALID_INPUT}, headers=headers)
    expected_status = 400
    print_output("Invalid Input", expected_status, r.status_code)


def print_output(test_type, expected_status, status_code):
    output = f"""
============================
  {test_type} Test
============================
| Expected Status: {expected_status}
| Actual Status: {status_code}
| Result: {"SUCCESS" if status_code == expected_status else "FAILURE"}
"""
    print(output)     

if __name__ == "__main__":
    token = get_token()
    test_invalid_input(token)
    test_valid_prediction(token)
