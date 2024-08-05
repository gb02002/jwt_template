from backend.core.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class Items(Base):
    __tablename__ = "items"

    title: Mapped[str] = mapped_column(String(255))
    author_id: Mapped[str] = mapped_column(String(60), index=True)
    views: Mapped[int] = mapped_column()
    position: Mapped[int] = mapped_column()

    ordered_user: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user: Mapped["Users"] = relationship("Users", back_populates="items")
