from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
class LeaveType(Base):
    __tablename__ = "leave_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    max_days = Column(Integer, nullable=False)
    description = Column(String)
    is_deleted = Column(Boolean, default=False)
    leaves = relationship("Leave", back_populates="leave_type")
