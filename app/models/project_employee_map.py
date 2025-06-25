from sqlalchemy import Column, Integer,String, Boolean, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# models/project_employee_map.py
class ProjectEmployeeMap(Base):
    __tablename__ = "project_employee_map"

    id = Column(Integer, primary_key=True, index=True)  # Auto-increment
    project_id = Column(Integer, ForeignKey("projects.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    from_date = Column(Date)
    to_date = Column(Date)
    remarks = Column(String)
    is_deleted = Column(Boolean, default=False)

    # ✅ Correct relationships
    project = relationship("Project", back_populates="employee_mappings")
    employee = relationship("Employee", back_populates="project_mappings")


