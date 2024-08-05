import datetime
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi.testclient import TestClient
import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException

from backend.core.exceptions.errors import TokenVerificationError
from main import app
from backend.api.dependencies import users_service, token_service
from backend.schemas.oauth_scheme import RefreshToken

client = TestClient(app)


class MockUserService:
    async def create(self, user):
        if user.username == "existing_user":
            raise IntegrityError("unique", {}, BaseException("unique"))
        return True

    async def get_single(self, username: str):
        if username == "existing_user":
            return MagicMock(id=1, password="hashed_password")
        return None


class MockTokenService:
    async def create(self, token):
        return "mock_refresh_token"
        # return MagicMock(token="mock_refresh_token")

    async def get_single(self, jti):
        if jti == "valid_jti":
            return RefreshToken(user_id=1, id=1, token='s', expires_at=datetime.datetime.now(), created_at=datetime.datetime.now())
        elif jti == "no_user_id":
            return RefreshToken(user_id=None, id=1, token='s', expires_at=datetime.datetime.now(), created_at=datetime.datetime.now())
        return None

    async def delete(self, user_id):
        return AsyncMock()


@pytest.fixture
def mock_verify_refresh_token():
    with patch('backend.api.users.users.verify_refresh_token') as mock:
        yield mock

app.dependency_overrides[users_service] = lambda: MockUserService()
app.dependency_overrides[token_service] = lambda: MockTokenService()

@pytest.fixture
def mock_token_service():
    return MockTokenService()


"""Registration"""


@pytest.mark.asyncio
async def test_register_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("users/registration", json={"username": "new_user", "password": "password"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() is True


@pytest.mark.asyncio
async def test_register_user_exists():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("users/registration", json={"username": "existing_user", "password": "password"})
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"].startswith("Exists")


"""Login"""


@pytest.mark.asyncio
async def test_login_success():
    response = client.post("users/login", json={'username': "existing_user", 'password': 'correct_password'})
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == "mock_access_token"
    assert response.cookies["refresh_token"] == "mock_refresh_token"


@pytest.mark.asyncio
async def test_login_user_not_found():
    response = client.post(
        "users/login",
        json={"username": "non_existent_user", "password": "correct_password"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No such user"


@pytest.mark.asyncio
async def test_login_incorrect_password(mock_auth_functions):
    mock_auth_functions[0].return_value = 0
    # Неправильный пароль
    response = client.post(
        "users/login",
        json={"username": "existing_user", "password": "incorrect_password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not correct pass"


@pytest.mark.asyncio
async def test_login_token_creation_failure():
    """Ошибка в создании токена"""

    async def mock_create(token):
        raise IntegrityError("unique", {}, BaseException("unique"))

    app.dependency_overrides[token_service] = lambda: MagicMock(create=mock_create)

    response = client.post(
        "users/login",
        json={"username": "existing_user", "password": "correct_password"}
    )
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json()["detail"].startswith("Fail to create tokens")

    app.dependency_overrides[token_service] = lambda: MockTokenService()


"""Logout"""


@pytest.mark.asyncio
async def test_logout_success():
    # app.dependency_overrides[token_service] = mock_auth_functions[3]
    response = client.post("users/logout", headers={"token": "token"})

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == {"msg": "Success"}


@pytest.mark.asyncio
async def test_logout_no_user(mock_auth_functions):
    mock_get_current_user = mock_auth_functions[2]
    mock_get_current_user.side_effect = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    response = client.post("users/logout", cookies={'refresh_token': 'mock_token'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "User not found"}

    mock_get_current_user.assert_called_once_with("mock_token")


@pytest.mark.asyncio
async def test_logout_no_token_to_delete(mock_auth_functions):
    mock_get_current_user = mock_auth_functions[2]
    mock_get_current_user.side_effect = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    response = client.post("users/logout", cookies={'refresh_token': 'mock_token'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "User not found"}

    mock_get_current_user.assert_called_once_with("mock_token")


"""Refresh"""


@pytest.mark.asyncio
async def test_check_token_success(mock_token_service, mock_verify_refresh_token):
    mock_verify_refresh_token.return_value = "valid_jti"
    app.dependency_overrides[token_service] = lambda: mock_token_service

    response = client.get("users/refresh", cookies={"refresh_token": "valid_refresh_token"})
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == {"access_token": "mock_access_token", 'token_type': 'Bearer'}  # Предполагается, что ваш create_access_token возвращает "mock_access_token"


@pytest.mark.asyncio
async def test_check_token_no_refresh_token(mock_token_service, mock_verify_refresh_token):
    mock_verify_refresh_token.side_effect = TokenVerificationError('No rf_token found')
    app.dependency_overrides[token_service] = lambda: mock_token_service

    response = client.get("users/refresh")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "No rf_token found"}


@pytest.mark.asyncio
async def test_check_token_invalid_token(mock_token_service, mock_verify_refresh_token):
    mock_verify_refresh_token.side_effect = TokenVerificationError('Invalid token')
    app.dependency_overrides[token_service] = lambda: mock_token_service

    response = client.get("users/refresh", cookies={"refresh_token": "invalid_refresh_token"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid token"}


@pytest.mark.asyncio
async def test_check_token_token_service_failure(mock_token_service, mock_verify_refresh_token):
    mock_verify_refresh_token.return_value = "unknown_jti"
    app.dependency_overrides[token_service] = lambda: mock_token_service

    response = client.get("users/refresh", cookies={"refresh_token": "valid_refresh_token"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}
