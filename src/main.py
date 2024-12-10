from fastapi import FastAPI
from fastapi.params import Depends

from src.database import get_db

app = FastAPI()


@app.get("/")
async def root(db=Depends(get_db)):
    return {"hello": "BE"}
