from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import get_settings

config = get_settings()

engine = create_engine(config.DATABASE_URL)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
