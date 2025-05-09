from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.base import get_async_session
from app.schemas.reservation import Reservation, ReservationCreate
from app.services.reservation import reservation_service

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.get("/", response_model=List[Reservation])
async def read_reservations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    return await reservation_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Reservation, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation: ReservationCreate,
    db: AsyncSession = Depends(get_async_session)
):
    return await reservation_service.create_reservation(db, reservation)


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    await reservation_service.delete(db, reservation_id)
    return None