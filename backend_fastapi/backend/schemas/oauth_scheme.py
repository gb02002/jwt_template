from .base_scheme import Base
from datetime import datetime


class AccessToken(Base):
    access_token: str
    token_type: str = "Bearer"


class RefreshToken(Base):
    id: int
    token: str
    user_id: int
    expires_at: datetime
    created_at: datetime


class CreateRefreshToken(Base):
    user_id: int


class RfTokenForUser(Base):
    token: str
    expires_at: datetime