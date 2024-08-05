from fastapi import APIRouter

from .items import router as items_router
from backend.api.users.users import router as user_router
from backend.api.users.profile import router as profile_router

main_router = APIRouter()

main_router.include_router(items_router, prefix='/items', tags=['items'])
main_router.include_router(user_router, prefix='/users', tags=['users'])
main_router.include_router(profile_router, prefix='/us', tags=['profile'])
