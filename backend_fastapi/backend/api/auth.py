from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, ExpiredSignatureError, jwt

from backend.core.project_config import settings
from backend.utils import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/clients/login")

