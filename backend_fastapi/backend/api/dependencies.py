from backend.services.item_service import ItemsService
from backend.services.user_service import UsersService
from backend.services.token_service import TokenService

from backend.repositories.users_repository import UsersRepository
from backend.repositories.tasks_repository import ItemsRepository
from backend.repositories.token_repository import TokenRepository


def users_service():
    return UsersService(UsersRepository)


def items_service():
    return ItemsService(ItemsRepository)


def token_service():
    return TokenService(TokenRepository)

# def admin_service():
#     return ItemsService(ItemsRepository)