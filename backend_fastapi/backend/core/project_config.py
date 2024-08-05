from datetime import datetime

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv
from zoneinfo import TZPATH, ZoneInfo


def manage_env(debug=True) -> str:
    if debug:
        path = find_dotenv('../../envs/.env.dev')
    else:
        path = find_dotenv('../../envs/.env.prod')
    return path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=manage_env(), env_file_encoding='utf-8')

    DB_ECHO: bool
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: str
    ALLOW_ORIGINS: str

    ADMIN_EMAIL: str
    ADMIN_FIRST_NAME: str
    ADMIN_LAST_NAME: str
    ADMIN_PASSWORD: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int
    REFRESH_TOKEN_EXPIRE_SECONDS: int
    ALGORITHM: str

    TZ: str

    # VERIFY_SECRET_KEY: str
    # SECRET_KEY_STAFF: str

    def build_postgres_dsn(self, migration=False) -> str:
        if migration:
            return (
                "postgresql+psycopg://"
                f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def build_redis_dsn(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
        # return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DATABASE}"

    def get_current_time(self) -> datetime:
        return datetime.now(ZoneInfo(self.TZ))



settings = Settings()
