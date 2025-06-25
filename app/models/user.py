from sqlalchemy import Column, Integer, String,Boolean,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    is_active = Column(Boolean, default=True)
    is_first_time_user = Column(Boolean, default=True)
    employee = relationship("Employee", foreign_keys=[employee_id])
    is_deleted = Column(Boolean, default=False)
    
