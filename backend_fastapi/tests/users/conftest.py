import pytest
import asyncio

from httpx import AsyncClient
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import create_async_engine
from main import app

from backend.models.base_model import Base
from backend.core.project_config import settings
from utils.create_superuser import admin_auto_creation

DATABASE_URL = settings.build_postgres_dsn()

engine_test = create_async_engine(DATABASE_URL, echo=settings.DB_ECHO)


@pytest.fixture(autouse=True)
def mock_auth_functions():
    """yield -> verify, access, get_user(token)"""
    with patch('backend.api.users.users.verify_password') as mock_verify_password, \
            patch('backend.api.users.users.create_access_token') as mock_create_access_token, \
            patch('backend.api.users.users.get_current_user') as mock_get_current_user:
            # patch('backend.api.users.users.token_service') as mock_token_service_async:

        mock_verify_password.return_value = True
        mock_create_access_token.return_value = "mock_access_token"
        mock_get_current_user.return_value = AsyncMock(id=1)
        # mock_token_service_async.return_value.delete = AsyncMock()

        # Передаем моки в тесты
        yield mock_verify_password, mock_create_access_token, mock_get_current_user


# @pytest.fixture(autouse=True, scope="session")
# async def prepare_db():
#     async with engine_test.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine_test.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture(autouse=True)
# async def admin_create():
#     await admin_auto_creation()
#

# @pytest.fixture(scope="session")
# async def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
#
#
# @pytest.fixture(scope="session")
# async def async_client():
#     async with AsyncClient(app=app, base_url="http://test") as cli:
#         yield cli