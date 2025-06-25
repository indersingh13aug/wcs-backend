from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class TaskComment(Base):
    __tablename__ = "task_comments"
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("task_assignments.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    comment = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    assignment = relationship("TaskAssignment", back_populates="comments")
    employee = relationship("Employee")
