from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    devices = relationship("Device", back_populates="location")