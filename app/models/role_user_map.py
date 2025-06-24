from sqlalchemy import Column,Boolean, Integer, ForeignKey, UniqueConstraint
from app.database import Base

class RoleUserMap(Base):
    __tablename__ = "role_user_map"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    is_deleted = Column(Boolean, default=False)
    __table_args__ = (UniqueConstraint("role_id", "employee_id", name="uix_role_employee"),)
