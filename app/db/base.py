from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.config import settings

# Преобразуем PostgresDsn в строку перед созданием engine
database_url = str(settings.POSTGRES_URL)

engine = create_async_engine(
    database_url,
    echo=True  # Логирование SQL (отключить в production)
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session