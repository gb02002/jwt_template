from backend.repositories.token_repository import TokenRepository
from backend.models.security_model import RefreshTokens
from backend.schemas.oauth_scheme import CreateRefreshToken
from backend.security import create_refresh_token


class TokenService:
    def __init__(self, token_repo: TokenRepository):
        self.token_repo: TokenRepository = token_repo(model=RefreshTokens)

    async def create(self, token: CreateRefreshToken):
        token_dict = token.model_dump()
        token = await self.token_repo.create(token_dict)

        return create_refresh_token(token.jti)

    async def update(self, data: dict, **filters):
        pass

    async def get_single(self, **filters):
        token = await self.token_repo.get_single(**filters)

        return token

    async def get_all(self):
        pass

    async def delete(self, **filters):
        await self.token_repo.delete(**filters)
