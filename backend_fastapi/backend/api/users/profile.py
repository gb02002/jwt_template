import logging

from typing import Annotated
from fastapi import APIRouter, Request, Depends

from backend.api.dependencies import users_service
from backend.schemas.user_scheme import UserViewModel
from backend.services.user_service import UsersService

router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.get("/profile", status_code=200, response_model=UserViewModel)
async def profile(request: Request, users_service: Annotated[UsersService, Depends(users_service)]):
    """profile getter"""

    user_info = users_service.get_single(id=request.state.user_id)
    return user_info