from fastapi import FastAPI
from api.storage import router as storage_router
from api.db import router as db_router
from api.posts import router as posts_router
from api.users import router as users_router
from core.middleware import log_requests
from core.logger import logger

app = FastAPI(
    title="FastAPI",
    description="API user <-> posts interaction",
    docs_url="/"
)


app.middleware("http")(log_requests)

logger.info("Starting application...")


app.include_router(users_router)
app.include_router(posts_router)
app.include_router(storage_router)
app.include_router(db_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Application started successfully")
