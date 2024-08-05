from functools import wraps
from fastapi import HTTPException, status


def isAdmin(func):
    @wraps(func)
    async def has_permission(**kwargs):
        current_staff = kwargs["current_staff"]

        if not current_staff.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )

        return await func(**kwargs)

    return has_permission

