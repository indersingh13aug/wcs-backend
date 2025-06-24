from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from app.database import Base
from sqlalchemy.orm import relationship
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    client_id = Column(Integer, ForeignKey("clients.id"))
    is_deleted = Column(Boolean, default=False)

    # ✅ Add this
    employee_mappings = relationship("ProjectEmployeeMap", back_populates="project")
