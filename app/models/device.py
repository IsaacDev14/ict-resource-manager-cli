from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    status = Column(Enum("available", "assigned", "damaged", name="status_enum"), default="available")
    location_id = Column(Integer, ForeignKey("locations.id"))


    #Realationships
    location = relationship("Location", back_populates="devices")
    assigmnents = relationship("Assignment", back_populates="devices")
    maintenance_logs = relationship("Maintenance", back_populations="devices")