from pydantic import Field
from typing import Optional
from app.schemas.base import BaseSchema


class TableBase(BaseSchema):
    name: str = Field(..., example="Table 1")
    seats: int = Field(..., gt=0, example=4)
    location: str = Field(..., example="Near window")


class TableCreate(TableBase):
    pass


class TableUpdate(BaseSchema):
    name: Optional[str] = Field(None, example="Table 1")
    seats: Optional[int] = Field(None, gt=0, example=4)
    location: Optional[str] = Field(None, example="Near window")


class Table(TableBase):
    id: int

    class Config:
        from_attributes = True