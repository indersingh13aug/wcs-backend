from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class TaskAssignment(Base):
    __tablename__ = "task_assignments"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    start_date = Column(Date)
    end_date = Column(Date)

    project = relationship("Project")
    task = relationship("Task")
    employee = relationship("Employee")
    comments = relationship("TaskComment", back_populates="assignment", cascade="all, delete")
