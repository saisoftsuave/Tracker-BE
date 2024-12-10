from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    HOST: str
    DATABASE_URL: str
    TEST_DATABASE_URL: str

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
