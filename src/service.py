import numpy as np
import bentoml
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from datetime import datetime, timedelta

JWT_SECRET_KEY = "your_jwt_secret_key_here"
JWT_ALGORITHM = "HS256"

USERS = {
    "user123": "password123",
    "user456": "password456"
}

CLASSIFIER_NAME = "random_forest_regressor_model"


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/v1/models/rfclassifierservice/predict":
            token = request.headers.get("Authorization")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Missing authentication token"})
            try:
                token = token.split()[1]  
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})
            request.state.user = payload.get("sub")
        response = await call_next(request)
        return response

class InputModel(BaseModel):
    gre_score: float = Field(alias="GRE Score")
    toefl_score: float = Field(alias="TOEFL Score")
    university_rating: float = Field(alias="University Rating")
    sop: float = Field(alias="SOP")
    lor: float = Field(alias="LOR")
    cgpa: float = Field(alias="CGPA")
    research: int = Field(alias="Research")
    
def create_jwt_token(user_id: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": user_id, "exp": expiration}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


@bentoml.service
class RFClassifierService:
    def __init__(self) -> None:
        self.model = bentoml.sklearn.load_model(f"{CLASSIFIER_NAME}:latest")

    @bentoml.api
    def login(self, credentials: dict) -> dict:
        username = credentials.get("username")
        password = credentials.get("password")
        if username in USERS and USERS[username] == password:
            token = create_jwt_token(username)
            return {"token": token}
        else:
            return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

    @bentoml.api
    def predict(self, input_data: InputModel) -> dict:
        input_series = np.array([
            input_data.gre_score,
            input_data.toefl_score,
            input_data.university_rating,
            input_data.sop,
            input_data.lor,
            input_data.cgpa,
            input_data.research
        ])

        result = self.model.predict(input_series.reshape(1, -1))

        return {"prediction": result.tolist()}

RFClassifierService.add_asgi_middleware(JWTAuthMiddleware)