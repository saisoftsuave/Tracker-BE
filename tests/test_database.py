import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.config import get_settings, Settings
from src.database import get_db, Base
from src.main import app

DATABASE_URL = get_settings().TEST_DATABASE_URL
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


def get_test_settings():
    return Settings(
        POSTGRES_USER="test_user",
        POSTGRES_PASSWORD="test_password",
        POSTGRES_DB="test_db",
        HOST="localhost",
        DATABASE_URL="sqlite:///./test.db",
        TEST_DATABASE_URL="sqlite:///./test_test.db"
    )


# app.dependency_overrides[get_settings()] = get_test_settings()
