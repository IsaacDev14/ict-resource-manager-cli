# app/models/device.py

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    status = Column(Enum("available", "assigned", "damaged", name="status_enum"), default="available")
    location_id = Column(Integer, ForeignKey("locations.id"))

    # Relationships
    location = relationship("Location", back_populates="devices")
    assignments = relationship("Assignment", back_populates="device")  # fixed here
    maintenance_logs = relationship("MaintenanceLog", back_populates="device")
