from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.table import Table
from app.schemas.table import TableCreate, TableUpdate
from app.services.base import BaseService


class TableService(BaseService[Table, TableCreate, TableUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: TableCreate) -> Table:
        # проверка на уникальности (существует ли уже таблица с таким именем)
        result = await db.execute(select(Table).where(Table.name == obj_in.name))
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Table with this name already exists",
            )
        return await super().create(db, obj_in=obj_in)


table_service = TableService(Table)