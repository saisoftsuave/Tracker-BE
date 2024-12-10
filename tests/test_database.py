import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.database import get_db, Base
from src.main import app

load_dotenv()
DATABASE_URL = os.getenv('TEST_DATABASE_URL')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

clint = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    setup_db()
    try:
        yield db
    finally:
        db.close()
        teardown_db()


app.dependency_overrides[get_db] = override_get_db


def setup_db():
    Base.metadata.create_all(bind=engine)


def teardown_db():
    Base.metadata.drop_all(bind=engine)
