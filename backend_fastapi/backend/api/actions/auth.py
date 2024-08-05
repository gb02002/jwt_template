from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, ExpiredSignatureError, jwt

from backend.core.project_config import settings
from backend.schemas.user_scheme import UserViewModel
from backend.utils import verify_password
from backend.api.dependencies import users_service, token_service

# from app.api.dependencies import admin_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def get_current_user(
    token: str = Annotated[str, Depends(oauth2_scheme)],
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not Validate Credentials",
    )

    try:
        payload = jwt.decode(
            token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        jti = payload.get("jti")

        if jti is None:
            raise credentials_exception

    except (JWTError, AttributeError):
        raise credentials_exception

    token_instance = await token_service().get_single(jti=jti)
    if not token_instance:
        raise credentials_exception

    return token_instance.user_id

#
# async def get_current_staff(token: str = Annotated[str, Depends(oauth2_scheme)]):
#
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not Validate Credentials",
#     )
#
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY_STAFF, algorithms=[settings.ALGORITHM]
#         )
#         id = payload.get("id")
#
#         if id is None:
#             raise credentials_exception
#
#     except JWTError:
#         raise credentials_exception
#
#     staff = await staff_service().get_single(id=id)
#     if not staff:
#         raise credentials_exception
#
#     return staff


async def authenticate_client(username: str, password: str):
    client = await users_service().get_single(username=username)

    if not client:
        return False

    if not verify_password(password, client.password):
        return False

    return client

