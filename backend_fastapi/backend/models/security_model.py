from datetime import datetime, timedelta
from backend.core.project_config import settings

from backend.core.database import Base

from sqlalchemy import func, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship


class RefreshTokens(Base):
    __tablename__ = 'refresh_tokens'

    jti: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    expires_at: Mapped[datetime] = mapped_column(
        default=lambda: settings.get_current_time() + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS),
        type_=DateTime(timezone=True)
    )

    user: Mapped["Users"] = relationship(back_populates="refresh_tokens", single_parent=True)

    __mapper_args__ = (
    )

    def __repr__(self):
        return (f"{self.__class__.__name__[:-1]} with id={self.id}, "
                f"life of {timedelta(self.expires_at - settings.get_current_time())} for user №{self.user_id}")
