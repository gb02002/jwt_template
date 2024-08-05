from datetime import timedelta, datetime
from jose import jwt

from backend.core.project_config import settings


def create_verification_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, settings.VERIFY_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt

