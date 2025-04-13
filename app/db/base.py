from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import settings

# Создание асинхронного движка БД
engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=True  # Логирование SQL-запросов (отключить в production)
)

# Фабрика асинхронных сессий
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False  # Позволяет работать с объектами после коммита
)

# Генератор асинхронных сессий для использования в зависимостях FastAPI
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:

    async with async_session_maker() as session:
        yield session