from backend.schemas.user_scheme import UserCreate, UserAuth
from backend.repositories.tasks_repository import ItemsRepository

from backend.models.item_model import Items


class ItemsService:
    def __init__(self, item_repo: ItemsRepository):
        self.item_repo: ItemsRepository = item_repo(model=Items)

    async def create(self, item):
        item_dict = item.model_dump()
        item = await self.item_repo.create(item_dict)

        return item

    async def update(self, data: dict, **filters):
        item_dict = data.model_dump()
        updated_item = await self.item_repo.update(item_dict, **filters)

        return updated_item

    async def get_single(self, **filters):
        item = await self.item_repo.get_single(**filters)
        return item

    async def get_all(self):
        get_all_items = await self.item_repo.get_all()
        return get_all_items
