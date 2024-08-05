import logging

from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Request, Depends
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

from backend.api.actions.auth import get_current_user
from backend.api.dependencies import users_service, token_service
from backend.core.exceptions.errors import TokenVerificationError
from backend.core.project_config import settings
from backend.schemas.user_scheme import UserCreate, UserAuth
from backend.schemas.oauth_scheme import CreateRefreshToken
from backend.security import create_access_token, verify_refresh_token
from backend.schemas.oauth_scheme import AccessToken
from backend.services.token_service import TokenService
from backend.services.user_service import UsersService
from backend.utils import verify_password

router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Ручка для регистрации нового пользователя
@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, users_service: Annotated[UsersService, Depends(users_service)]):
    try:
        await users_service.create(user)
    except IntegrityError as err:
        if "unique" in str(err.orig):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Exists")
        logger.error(f"IntegrityError: {err.orig}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Internal error")

    return True


# Ручка для логина пользователя
@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login(
        form_data: UserAuth,
        users_service: Annotated[UsersService, Depends(users_service)],
        token_service: Annotated[TokenService, Depends(token_service)]
):
    user = await users_service.get_single(username=form_data.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not correct pass")

    access_token = create_access_token(data={'sub': user.id})

    try:
        rf_token = await token_service.create(token=CreateRefreshToken(user_id=user.id))
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Fail to create tokens, {err}")

    response = JSONResponse(content=access_token, status_code=status.HTTP_202_ACCEPTED)
    response.set_cookie(
        key='refresh_token',
        value=rf_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        path="/users/auth"
    )

    return response


# Ручка для логина пользователя
@router.post("/auth/logout", status_code=status.HTTP_202_ACCEPTED)
async def logout(request: Request, token_service: Annotated[TokenService, Depends(token_service)]):
    """Retreat rf_token"""
    user_id = await get_current_user(request.cookies.get('refresh_token'))

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    await token_service.delete(user_id=user_id)

    return {"msg": "Success"}


@router.get("/auth/refresh", status_code=status.HTTP_202_ACCEPTED, response_model=AccessToken)
async def check_token(request: Request, token_service: Annotated[TokenService, Depends(token_service)]):
    """Check rf and return access token"""
    # Надо разобраться с логикой ошибок. Тут их слишком много
    try:
        rf_token = request.cookies.get('refresh_token')
        if rf_token:
            jti = verify_refresh_token(rf_token=rf_token)
            token = await token_service.get_single(jti=jti)

            if not hasattr(token, 'user_id'):
                raise TokenVerificationError("User not found")

            token = create_access_token(data={'sub': token.user_id})
            return AccessToken(access_token=token)
        raise TokenVerificationError('No rf_token found')

    except TokenVerificationError as e:
        if "expired" in e.message or "No rf_token found" in e.message or "Invalid token" in e.message:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)
        elif "User not found" in e.message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message)
    except Exception as e:
        logger.error(e)
