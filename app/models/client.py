from sqlalchemy import Column, Integer, String,Boolean
from app.database import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gst_number = Column(String, nullable=True)
    company = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
