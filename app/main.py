from fastapi import FastAPI
from app.routers import tables, reservations
from app.db.base import engine
from app.models.base import Base  # Импорт Base из правильного места
from contextlib import asynccontextmanager
from typing import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Обработчик жизненного цикла приложения"""
    # Создание таблиц при старте (в production используйте миграции!)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # При необходимости можно добавить логику завершения


app = FastAPI(
    title="Restaurant Booking API",
    description="API for booking tables in a restaurant",
    version="0.1.0",
    lifespan=lifespan,  # Регистрация обработчика жизненного цикла
)

# Подключение роутеров
app.include_router(tables.router)
app.include_router(reservations.router)


@app.get("/")
async def root():
    return {"message": "Restaurant Booking API"}