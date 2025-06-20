from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    id : int
    user_id: int
    first_name: str
    middle_name: str
    last_name: str
    date_of_joining: str
    email: str
    role_id: int
    department_id: int


class EmployeeCreate(BaseModel):
    user_id: int
    first_name: str
    middle_name: str
    last_name: str
    date_of_joining: str
    email: str
    role_id: int
    department_id: int


class DepartmentOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }
class RoleOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class EmployeeOut(EmployeeBase):
    id: int
    user_id: int
    first_name: str
    middle_name: str
    last_name: str
    email: str
    date_of_joining: str
    role_id: int
    department_id: int
    status: str
    role: Optional[RoleOut] = None
    department: Optional[DepartmentOut] = None
    model_config = {
        "from_attributes": True
    }
