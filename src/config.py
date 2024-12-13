from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    HOST: str
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
 


Config =  Settings()
