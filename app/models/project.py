from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from app.database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    client_id = Column(Integer, ForeignKey("clients.id"))
    assigned_team = Column(String)  # e.g., "1,2,3"
    is_deleted = Column(Boolean, default=False)