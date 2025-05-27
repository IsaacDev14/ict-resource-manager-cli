from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    contact_info = Column(String)


    # One user can be assigned multiple devices
    assignments = relationship("Assignment", back_populates="user")