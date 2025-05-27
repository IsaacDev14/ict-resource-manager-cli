from sqlalchemy import Column, Integer, String, Enum
from app.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    status = Column(Enum("available", "assigned", "damaged", name="status_enum"), default="available")
    location = Column(String)