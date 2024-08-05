from datetime import datetime

from sqlalchemy import func, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from backend.core.project_config import settings


class Base(DeclarativeBase):
    __abstarct__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: settings.get_current_time(),
        type_=DateTime(timezone=True)
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"
