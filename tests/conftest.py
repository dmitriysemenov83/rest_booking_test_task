import asyncio
import os

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.db.base import get_async_session
from app.models.base import Base

from dotenv import load_dotenv
load_dotenv()


# Загружаем тестовый URL из .env
DATABASE_TEST_URL = os.getenv("POSTGRES_TEST_URL")
if not DATABASE_TEST_URL:
    raise RuntimeError("POSTGRES_TEST_URL is not set in the environment")

engine_test = create_async_engine(DATABASE_TEST_URL, echo=False)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Создание таблиц перед тестами
@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Сессия БД для тестов
@pytest_asyncio.fixture()
async def async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


# HTTP клиент с переопределением зависимостей
@pytest_asyncio.fixture()
async def async_client(async_session: AsyncSession) -> AsyncClient:
    async def override_get_async_session():
        yield async_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
