import pytest
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from jose import jwt
from starlette import status

from backend.core.exceptions.errors import TokenVerificationError
from backend.core.project_config import settings

from starlette.testclient import TestClient

from backend.core.middleware.authentication_middleware import VerificationMiddleware


@pytest.fixture
def app():
    app = FastAPI()

    @app.get("/protected")
    async def protected_route(request: Request):
        return JSONResponse(content={"message": "This is a protected route"})

    @app.get("/users")
    async def docs_route():
        return JSONResponse(content={"message": "This is the users route"})

    app.add_middleware(VerificationMiddleware)
    return app


# Клиент для тестирования
@pytest.fixture
def client(app):
    return TestClient(app)


def test_exempt_paths(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == {"message": "This is the users route"}


def test_protected_route_no_token(client):
    with pytest.raises(TokenVerificationError) as exc_info:
        client.get("/protected")
    assert str(exc_info.value.message) == "No token"


def test_protected_route_with_valid_token(client):
    valid_token = jwt.encode({"sub": "user_id"}, settings.ACCESS_SECRET_KEY, algorithm=settings.ALGORITHM)
    response = client.get("/protected", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "This is a protected route"}


def test_protected_route_with_invalid_token(client):
    with pytest.raises(TokenVerificationError) as exc_info:
        client.get("/protected", headers={"Authorization": "invalid_token"})
    assert str(exc_info.value.message) == "No token"


def test_protected_route_with_no_token(client):
    with pytest.raises(TokenVerificationError) as exc_info:
        client.get("/protected")
    assert str(exc_info.value.message) == "No token"
