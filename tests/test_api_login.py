import pytest
import requests

LOGIN_URL = "http://127.0.0.1:3000/login"

CREDENTIALS={
    "user123": ("password123", 200),
    "userfalsch": ("passwordflasch", 401)
}

def test_login(username, password):
    """Verify that the API returns a valid JWT token for correct user credentials."""
    response = requests.post(
        LOGIN_URL,
        json={"credentials": {"username": username, "password": password}}
    )
    return response.status_code
    

def print_output(username, password, expected_status, status_code):
    output = f"""
============================
  Login Test
============================
| username: {username}
| password: {password}
| Expected Status: {expected_status}
| Actual Status: {status_code}
| Result: {"SUCCESS" if status_code == expected_status else "FAILURE"}
"""
    print(output)    

def main():
    status_code=test_login(username, password)
    print_output(username, password, expected_status, status_code)


if __name__ == "__main__":

    for username, (password, expected_status) in CREDENTIALS.items():
       main()
