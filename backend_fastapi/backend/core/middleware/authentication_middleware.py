from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from starlette.responses import Response

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from backend.core.project_config import settings
from backend.core.exceptions.errors import TokenVerificationError


class VerificationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exempt_path: list[str] = None):
        super().__init__(app)
        self.exempt_paths = exempt_path or ['/docs', '/openapi.json', '/users']

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if self.is_exempt_path(request.url.path):
            response = await call_next(request)
        else:
            await self.verify_token(request)
            response = await call_next(request)
        return response

    def is_exempt_path(self, path: str) -> bool:
        return any(path.startswith(exempt_path) for exempt_path in self.exempt_paths)

    @staticmethod
    async def verify_token(request: Request) -> None:
        authorization = request.headers.get("Authorization")

        if authorization is None or not authorization.startswith("Bearer "):
            raise TokenVerificationError(message="No token")

        token = authorization.split("Bearer ")[1]

        try:
            payload = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM])
            request.state.user_id = payload.get('sub')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
