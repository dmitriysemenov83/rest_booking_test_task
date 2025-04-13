from datetime import datetime, timedelta
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationCreate, ReservationUpdate
from app.services.base import BaseService


class ReservationService(BaseService[Reservation, ReservationCreate, ReservationUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: ReservationCreate) -> Reservation:
        # проверка на уникальность (существует ли уже бронирование на эту дату)
        table = await db.execute(select(Table).where(Table.id == obj_in.table_id))
        table = table.scalars().first()
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found",
            )

        # Проверка на наличие перекрывающихся бронирований
        reservation_start = obj_in.reservation_time
        reservation_end = reservation_start + timedelta(minutes=obj_in.duration_minutes)

        overlapping = await db.execute(
            select(Reservation)
            .where(Reservation.table_id == obj_in.table_id)
            .where(
                (
                    (Reservation.reservation_time <= reservation_start)
                    & (
                        Reservation.reservation_time
                        + timedelta(minutes=Reservation.duration_minutes)
                        > reservation_start
                    )
                )
                | (
                    (Reservation.reservation_time < reservation_end)
                    & (
                        Reservation.reservation_time
                        + timedelta(minutes=Reservation.duration_minutes)
                        >= reservation_end
                    )
                )
                | (
                    (Reservation.reservation_time >= reservation_start)
                    & (
                        Reservation.reservation_time
                        + timedelta(minutes=Reservation.duration_minutes)
                        <= reservation_end
                    )
                )
            )
        )

        if overlapping.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The table is already booked for this time slot",
            )

        return await super().create(db, obj_in=obj_in)


reservation_service = ReservationService(Reservation)