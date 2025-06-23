from sqlalchemy import Column, Integer, String,Boolean
from app.database import Base
from sqlalchemy.orm import relationship
class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    path = Column(String, unique=True)
    group_name = Column(String, unique=False,nullable=True) 
    is_deleted = Column(Boolean, default=False)
    access = relationship("RolePageAccess", back_populates="page", cascade="all, delete")