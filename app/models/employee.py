from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id  = Column(Integer, ForeignKey("users.id"))
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_joining= Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    status = Column(String, default="Active")
    is_deleted = Column(Boolean, default=False)
    
    # Use full module path to avoid circular import issues
    role = relationship("Role", back_populates="employees")
    department = relationship("Department", back_populates="employees")