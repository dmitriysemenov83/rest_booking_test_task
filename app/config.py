from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    POSTGRES_URL: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/restaurant_booking"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()