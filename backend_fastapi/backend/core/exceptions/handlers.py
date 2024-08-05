from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from .errors import TokenVerificationError


def token_exception_handler(request: Request, exc: TokenVerificationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=f"Not authenticated, {exc.message}"
    )
