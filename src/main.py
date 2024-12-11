from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from src.core.routes import Routes
from src.database import get_db, engine
from src.model.auth.user_model import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get(Routes.ROOT_URL)
async def root(db: Session = Depends(get_db)):
    user = User(user_id=uuid4(), first_name="sai", last_name="babu", email_id="sai.babu@softsuave.org",
                hashed_password="sai@123")
    db.add(user)
    db.commit()
    return {"hello": "world"}
