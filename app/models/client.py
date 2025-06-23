from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    client_code=Column(String, nullable=True)
    contact_person = Column(String)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    addressline1 = Column(String, nullable=False)
    addressline2 = Column(String, nullable=False)
    state=Column(String, nullable=False)
    country =Column(String, nullable=False)
    pincode=Column(String, nullable=False)
    gst_number = Column(String, unique=True)
    is_deleted = Column(Boolean, default=False)

    # Optional relations
    # sales = relationship("Sales", back_populates="client")
    
