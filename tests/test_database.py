from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from starlette.testclient import TestClient

from src.main import app


class TestSettings:
        POSTGRES_USER="test_user",
        POSTGRES_PASSWORD="test_password",
        POSTGRES_DB="test_db",
        HOST="localhost",
        DATABASE_URL="sqlite:///./test.db",
        TEST_DATABASE_URL="sqlite:///./test_test.db"



DATABASE_URL = TestSettings.TEST_DATABASE_URL
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

#
# app.dependency_overrides[get_db] = override_get_db
#

def setup_db():
    SQLModel.metadata.create_all(bind=engine)


def teardown_db():
    SQLModel.metadata.drop_all(bind=engine)



# app.dependency_overrides[get_settings()] = get_test_settings()
