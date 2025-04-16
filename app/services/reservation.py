from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from fastapi import HTTPException, status
from datetime import timedelta
from sqlalchemy import select


class ReservationService:
    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Reservation]:
        result = await db.execute(select(Reservation).offset(skip).limit(limit))
        return result.scalars().all()

    async def get(self, db: AsyncSession, reservation_id: int) -> Reservation:
        result = await db.execute(
            select(Reservation)
            .where(Reservation.id == reservation_id)
        )
        reservation = result.scalars().first()
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Бронь не найдена"
            )
        return reservation

    async def create_reservation(self, db: AsyncSession, reservation_data: ReservationCreate) -> Reservation:
        reservation_start = reservation_data.reservation_time
        reservation_end = reservation_start + timedelta(minutes=reservation_data.duration_minutes)

        # проверка конфликтов и пересечений
        existing = await db.execute(
            select(Reservation)
            .where(Reservation.table_id == reservation_data.table_id)
            .where(
                Reservation.reservation_time < reservation_end,
                Reservation.reservation_time + timedelta(minutes=60) > reservation_start
            )
        )

        if existing.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Booking conflict",
                    "message": "Столик уже забронирован на выбранное время"
                }
            )

        reservation = Reservation(
            customer_name=reservation_data.customer_name,
            table_id=reservation_data.table_id,
            reservation_time=reservation_data.reservation_time,
            duration_minutes=reservation_data.duration_minutes
        )

        db.add(reservation)
        await db.commit()
        await db.refresh(reservation)
        return reservation

    async def delete(self, db: AsyncSession, reservation_id: int) -> None:
        reservation = await self.get(db, reservation_id)
        await db.delete(reservation)
        await db.commit()


reservation_service = ReservationService()
