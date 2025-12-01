import requests

# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3000/login"
predict_url = "http://127.0.0.1:3000/predict"

# Data for login - must match the service signature
login_payload = {
    "credentials": {
        "username": "user123",
        "password": "password123"
    }
}

# Send a POST request to the login endpoint
login_response = requests.post(
    login_url,
    headers={"Content-Type": "application/json"},
    json=login_payload
)

# Check if the login was successful
if login_response.status_code == 200:
    token = login_response.json().get("token")
    print("Token JWT obtained:", token)

    # Data to be sent to the prediction endpoint
    prediction_payload = {
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

    # Send a POST request to the prediction
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=prediction_payload
    )

    print("Prediction API response:", response.text)
else:
    print("Error during login:", login_response.text)