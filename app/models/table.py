from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=False)

    reservations = relationship('Reservation', back_populates='table')

    def __repr__(self):
        return f"Table(id={self.id}, name={self.name}, seats={self.seats}, location={self.location})"

    def __str__(self):
        return f"Table(id={self.id}, name={self.name}, seats={self.seats}, location={self.location})"