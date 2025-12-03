import requests

login_url = "http://127.0.0.1:3000/login"
predict_url = "http://127.0.0.1:3000/predict"

login_payload = {
    "credentials": {
        "username": "user123",
        "password": "password123"
    }
}

login_response = requests.post(
    login_url,
    headers={"Content-Type": "application/json"},
    json=login_payload
)

if login_response.status_code == 200:
    token = login_response.json().get("token")
    print("Token JWT obtained:", token)

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