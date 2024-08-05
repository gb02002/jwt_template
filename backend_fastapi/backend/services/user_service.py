from backend.schemas.user_scheme import UserCreate, UserAuth
from backend.repositories.users_repository import UsersRepository

from backend.models.user_model import Users
# from backend.models.development import Staff


class UsersService:
    def __init__(self, user_repo: UsersRepository):
        self.user_repo: UsersRepository = user_repo(model=Users)

    async def create(self, user):
        user_dict = user.model_dump()
        user = await self.user_repo.create(user_dict)

        return user

    async def update(self, data: dict, **filters):
        user_dict = data.model_dump()
        updated_user = await self.user_repo.update(user_dict, **filters)

        return updated_user

    async def get_single(self, **filters):
        user = await self.user_repo.get_single(**filters)
        return user

    async def get_all(self):
        get_all_users = await self.user_repo.get_all()
        return get_all_users


# class StaffService:
#     def __init__(self, staff_repo: UsersRepository):
#         self.staff_repo: UsersRepository = staff_repo(model=Staff)
#
#     async def create(self, staff: StaffCreationModel) -> StaffCreationModel:
#         staff_dict = staff.model_dump()
#         staff = await self.staff_repo.create(staff_dict)
#
#         return staff
#
#     async def update(self, data: dict, **filters):
#         staff_dict = data.model_dump()
#         updated_staff = await self.staff_repo.update(staff_dict, **filters)
#
#         return updated_staff
#
#     async def get_single(self, **filters):
#         staff = await self.staff_repo.get_single(**filters)
#         return staff
#
#     async def delete(self, **filters):
#         await self.staff_repo.delete(**filters)
#
#     async def get_all(self):
#         get_all_users = await self.staff_repo.get_all()
#         return get_all_users