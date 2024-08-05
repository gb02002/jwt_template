import asyncio

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.router import main_router
from backend.core.exceptions.errors import TokenVerificationError
from backend.core.exceptions.handlers import token_exception_handler
from backend.core.middleware.authentication_middleware import VerificationMiddleware
from backend.core.project_config import settings
from utils.setup import prepare_db


def get_application() -> FastAPI:
    application = FastAPI(title="My_FastAPI", debug=settings.DEBUG, version=settings.VERSION)

    application.include_router(main_router)
    application.add_middleware(
        CORSMiddleware, allow_methods=["*"], allow_headers=["*"],
        allow_origins=[settings.ALLOW_ORIGINS], allow_credentials=True
    )
    application.add_middleware(VerificationMiddleware)

    application.add_exception_handler(TokenVerificationError, token_exception_handler)

    return application


app: FastAPI = get_application()

if __name__ == "__main__":
    asyncio.run(prepare_db())
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
