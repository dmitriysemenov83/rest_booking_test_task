from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.base import get_async_session
from app.schemas.table import Table, TableCreate
from app.services.table import table_service

router = APIRouter(prefix="/tables", tags=["tables"])

@router.get("/", response_model=List[Table])
async def read_tables(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    return await table_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Table, status_code=201)
async def create_table(
    table: TableCreate,
    db: AsyncSession = Depends(get_async_session)
):
    return await table_service.create(db, obj_in=table)

@router.delete("/{table_id}", status_code=204)
async def delete_table(
    table_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    await table_service.delete(db, id=table_id)
    return None