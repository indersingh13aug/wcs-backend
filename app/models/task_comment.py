from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime,String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class TaskComment(Base):
    __tablename__ = "task_comments"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("task_assignments.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    comment = Column(Text, nullable=False)
    status = Column(String, nullable=True)
    assigned_to_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # ✅ Define relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    assigned_to = relationship("Employee", foreign_keys=[assigned_to_id])
    assignment = relationship("TaskAssignment", back_populates="comments")
