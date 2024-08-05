import asyncio

from utils.create_superuser import admin_auto_creation
from backend.core.database import init_models


async def prepare_db():
    await init_models()
    await admin_auto_creation()


if __name__ == "__main__":
    asyncio.run(prepare_db())