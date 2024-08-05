from datetime import datetime, timedelta
from typing import List, Optional
from backend.core.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime
from .security_model import RefreshTokens
from .item_model import Items
from ..core.project_config import settings


class Users(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)

    first_name: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    password: Mapped[str]

    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: settings.get_current_time(),
        onupdate=lambda: settings.get_current_time(),
        type_=DateTime(timezone=True)
    )

    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    items: Mapped[List["Items"]] = relationship(back_populates="user")
    refresh_tokens: Mapped[List["RefreshTokens"]] = relationship(back_populates="user")

    def __repr__(self):
        return (f"{self.__class__.__name__[:-1]} with id={self.id}, "
                f"")
