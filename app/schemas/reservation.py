from datetime import datetime
from pydantic import Field, field_validator, ConfigDict
from typing import Optional
from app.schemas.base import BaseSchema


class ReservationBase(BaseSchema):
    customer_name: str = Field(..., json_schema_extra={"example": "John Doe"})
    table_id: int = Field(..., gt=0, json_schema_extra={"example": 1})
    reservation_time: datetime = Field(..., json_schema_extra={"example": "2025-01-01T12:00:00"})
    duration_minutes: int = Field(..., gt=0, le=240, json_schema_extra={"example": 60})


class ReservationCreate(ReservationBase):
    @field_validator('reservation_time')
    def validate_reservation_time(cls, v: datetime) -> datetime:
        if v.minute not in (0, 15, 30, 45):
            raise ValueError("Время бронирования должно быть указано с интервалом в 15 минут.")
        return v


class ReservationUpdate(BaseSchema):
    customer_name: Optional[str] = Field(None, json_schema_extra={"example": "John Doe"})
    table_id: Optional[int] = Field(None, gt=0, json_schema_extra={"example": 1})
    reservation_time: Optional[datetime] = Field(None, json_schema_extra={"example": "2023-01-01T12:00:00"})
    duration_minutes: Optional[int] = Field(None, gt=0, le=240, json_schema_extra={"example": 60})


class Reservation(ReservationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
