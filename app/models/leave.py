from sqlalchemy import Column, Integer, String, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(String(20), default="Pending")
    leave_type_id =  Column(Integer, ForeignKey("leave_types.id"), nullable=True)

    employee = relationship("Employee", back_populates="leaves")
    leave_type = relationship("LeaveType", back_populates="leaves")