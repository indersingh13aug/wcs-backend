from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_person = Column(String)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    address = Column(String)
    gst_number = Column(String, unique=True)
    is_deleted = Column(Boolean, default=False)
