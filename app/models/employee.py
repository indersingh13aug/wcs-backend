from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey,DateTime
from app.database import Base
from datetime import datetime

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id  = Column(Integer, ForeignKey("users.id"))
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_joining= Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    ro_id = Column(Integer, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    status=Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
    # ✅ Add this relationship
    department = relationship("Department", back_populates="employees")
    leaves = relationship("Leave", back_populates="employee")
    role = relationship("Role", back_populates="employees")
    project_mappings = relationship("ProjectEmployeeMap", back_populates="employee")
    # Add this inside Employee class
    images = relationship("EmployeeImage", back_populates="employee", cascade="all, delete-orphan")


    @property
    def full_name(self) -> str:
        return " ".join(
            str(part).strip() for part in [self.first_name, self.middle_name, self.last_name] if part is not None
        )
    
class EmployeeImage(Base):
    __tablename__ = "employee_images"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    image_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="images")