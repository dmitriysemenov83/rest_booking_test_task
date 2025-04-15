from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import tables, reservations
from app.db.base import engine
from app.models.base import Base
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Обработчик жизненного цикла приложения"""
    try:
        # Создаем таблицы (только для разработки!)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logging.info("Database tables created")
        yield
    except Exception as e:
        logging.error(f"Startup error: {e}")
        raise

app = FastAPI(
    title="Restaurant Booking API",
    lifespan=lifespan,
)

# Подключаем роутеры
app.include_router(tables.router)
app.include_router(reservations.router)

@app.get("/")
async def root():
    return {"message": "Restaurant Booking API"}