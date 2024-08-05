import re
from typing import Optional

from .base_scheme import Base

from pydantic import field_validator

from fastapi import HTTPException, status

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
USERNAME_LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Z]")
MAX_PASSWORD_LENGTH = 3


class UserCreate(Base):
    username: str
    password: str

    @field_validator("username")
    def validate_username(cls, value):
        if not USERNAME_LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_421_UNPROCESSABLE_ENTITY,
                detail="Username should contain only letters",
            )
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < MAX_PASSWORD_LENGTH:
            raise HTTPException(
                status_code=status.HTTP_421_UNPROCESSABLE_ENTITY,
                detail=f"Password can not contain less than {MAX_PASSWORD_LENGTH} symbols",
            )
        return value


class UserAuth(Base):
    username: str
    password: str


class UserViewModel(Base):
    id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_verified: bool
    is_superuser: bool
