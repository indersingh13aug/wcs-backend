from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)

    employees = relationship("Employee", back_populates="department")