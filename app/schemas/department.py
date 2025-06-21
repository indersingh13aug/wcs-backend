# app/schemas/department.py
from pydantic import BaseModel

class DepartmentBase(BaseModel):
    name: str
    description: str | None = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int
    is_deleted: bool

    model_config = {
        "from_attributes": True
    }
