from backend.core.project_config import settings
from backend.core.database import async_session
from backend.models.user_model import Users
from backend.utils import hash_password

from sqlalchemy import select


async def admin_auto_creation() -> Users:
    password = hash_password(settings.ADMIN_PASSWORD)

    async with async_session() as session:
        query = select(Users).filter_by(username=settings.ADMIN_EMAIL)
        admin_exists = await session.scalar(query)

        if admin_exists:
            return "Admin already exists"

        admin = Users(
            first_name=settings.ADMIN_FIRST_NAME,
            last_name=settings.ADMIN_LAST_NAME,
            username=settings.ADMIN_EMAIL,
            is_superuser=True,
            is_verified=True,
            password=password,
        )

        session.add(admin)
        await session.commit()
        await session.refresh(admin)

        return admin