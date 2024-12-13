from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import Config

async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,

)


async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependency for retrieving a database session
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session