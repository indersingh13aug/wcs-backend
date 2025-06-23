from sqlalchemy import Column, Integer, String, Boolean,ForeignKey, Date
from app.database import Base
from sqlalchemy.orm import relationship

class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    type_id = Column(Integer, ForeignKey("client_types.id"))

    contact_number = Column(String, nullable=False)
    contact_person = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, default="lead")  # lead, opportunity, active

    is_deleted = Column(Boolean, default=False)

    # client = relationship("Client", back_populates="sale")
    
    # role = relationship("Role", back_populates="roles")
    # service = relationship("Service", back_populates="services")
    # client_type = relationship("ClientType", back_populates="client_types")
