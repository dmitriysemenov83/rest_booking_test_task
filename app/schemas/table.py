from pydantic import Field, ConfigDict
from typing import Optional
from app.schemas.base import BaseSchema


class TableBase(BaseSchema):
    name: str
    seats: int
    location: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "name": "Table 1",
                    "seats": 4,
                    "location": "Near window"
                }
            ]
        }
    )


class TableCreate(TableBase):
    pass


class TableUpdate(BaseSchema):
    name: Optional[str] = None
    seats: Optional[int] = Field(default=None, gt=0)
    location: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Table 1",
                    "seats": 4,
                    "location": "Near window"
                }
            ]
        }
    )


class Table(TableBase):
    id: int
