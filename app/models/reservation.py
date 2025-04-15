from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    reservation_time = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    table = relationship("Table", back_populates="reservations")

    def __repr__(self):
        return (
            f"Reservation(id={self.id}, customer_name={self.customer_name}, "
            f"table_id={self.table_id}, reservation_time={self.reservation_time}, "
            f"duration_minutes={self.duration_minutes})"
        )

    def __str__(self):
        return (
            f"Reservation(id={self.id}, customer_name={self.customer_name}, "
            f"table_id={self.table_id}, reservation_time={self.reservation_time}, "
            f"duration_minutes={self.duration_minutes})"
        )
