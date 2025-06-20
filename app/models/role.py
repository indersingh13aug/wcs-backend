from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from app.database import Base
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  #
    is_deleted = Column(Boolean, default=False)
    employees = relationship("Employee", back_populates="role")
    