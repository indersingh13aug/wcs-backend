
from sqlalchemy import Column, Integer, ForeignKey,Boolean
from app.database import Base
from sqlalchemy.orm import relationship

class RolePageAccess(Base):
    __tablename__ = "role_page_access"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    page_id = Column(Integer, ForeignKey("pages.id"))

    view_access = Column(Boolean, default=False)
    apply_access = Column(Boolean, default=False)
    update_access = Column(Boolean, default=False)
    delete_access = Column(Boolean, default=False)

    role = relationship("Role", back_populates="access")
    page = relationship("Page", back_populates="access")