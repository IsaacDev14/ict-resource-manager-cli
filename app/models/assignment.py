# app/models/assignment.py

from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_date = Column(Date)
    return_date = Column(Date)

    # Relationships
    device = relationship("Device", back_populates="assignments")
    user = relationship("User", back_populates="assignments")
