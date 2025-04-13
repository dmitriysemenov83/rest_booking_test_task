from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    POSTGRES_URL: PostgresDsn = 'postgresql+asyncpg://postgres:postgres@localhost:5432/r_booking'
    SECRET_KEY: str = 'secret_key'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = '.env'


settings = Settings()