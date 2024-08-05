from datetime import timedelta, datetime
from typing import Optional

from jose import jwt

from backend.core.project_config import settings
from backend.core.exceptions.errors import TokenVerificationError


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def create_refresh_token(jti):
    to_encode = {
        "exp": datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_SECONDS),
        "jti": jti
    }

    encoded_jwt = jwt.encode(to_encode, key=settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def verify_refresh_token(rf_token: str) -> Optional[str]:
    try:
        payload = jwt.decode(rf_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        jti = payload.get("jti")

        if not jti:
            raise TokenVerificationError("Invalid token: 'jti' claim missing")

        return jti

    except jwt.ExpiredSignatureError:
        raise TokenVerificationError("Refresh token expired")

    except Exception as e:
        # Возвращаем общую ошибку, если произошла непредвиденная ошибка
        raise TokenVerificationError("Invalid refresh token")


def create_access_token_for_staff(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY_STAFF, settings.ALGORITHM)

    return encoded_jwt
