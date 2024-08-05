import uuid
from typing import TypeVar

from sqlalchemy import select, delete

from .base_repository import AbstractRepository
from backend.core.database import async_session
from backend.security import create_refresh_token


class TokenRepository(AbstractRepository):
    def __init__(self, model):
        self.model = model

    async def create(self, data: dict):
        async with async_session() as session:
            instance = self.model(**data)
            instance.jti = str(uuid.uuid4())

            session.add(instance)
            await session.commit()
            await session.refresh(instance)

            return instance

    async def get_single(self, **filters):
        async with async_session() as session:
            row = await session.execute(select(self.model).filter_by(**filters))
            if row:
                print(row)
                print("ТУТ надо сделать проверку на expire. Если что тут прямо тут удалить и вернуть None")
            return row.scalar_one_or_none()

    async def update(self, data: dict, **filters) -> TypeVar:
        pass

    async def delete(self, **filters) -> None:
        async with async_session() as session:
            await session.execute(delete(self.model).filter_by(**filters))
            await session.commit()
