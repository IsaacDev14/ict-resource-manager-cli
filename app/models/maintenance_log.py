from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base

class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    issue_description = Column(Text, nullable=False)
    repair_action = Column(Text)
    date = Column(Date)

    # Relationship to Device
    device = relationship("Device", back_populates="maintenance_logs")
