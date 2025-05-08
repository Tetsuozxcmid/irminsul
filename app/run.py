from fastapi import FastAPI
from appwrite.client import Client
from config import settings
from api.storage import router as storage_router
from api.db import router as db_router
from api.posts import router as posts_router
from api.users import router as users_router


app = FastAPI(
    title="FastAPI",
    description="API user <-> posts interaction",
    docs_url="/"
)


app.include_router(users_router)
app.include_router(posts_router)
app.include_router(storage_router)
app.include_router(db_router)
