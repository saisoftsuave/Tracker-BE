from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.routes import Routes
from src.database import get_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get(Routes.ROOT_URL)
async def root(db: AsyncSession = Depends(get_db)):
    return {"hello": "world"}
