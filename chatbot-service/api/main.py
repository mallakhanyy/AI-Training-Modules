from fastapi import FastAPI

from api.routes.chat import router as chat_router
from shared.config import settings


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
)

app.include_router(chat_router)