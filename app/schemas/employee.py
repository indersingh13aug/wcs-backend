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





class RoleOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }




class DepartmentOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }



class EmployeeOut(BaseModel):
    id: int
    user_id: int
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: str
    date_of_joining: str  # If you want, use `date` type if it's parsed as `datetime.date`
    status: str
    role: Optional[RoleOut] = None
    department: Optional[DepartmentOut] = None
    ro_name: Optional[str] = None  # RO full name added manually in backend

    model_config = {
        "from_attributes": True
    }



class ITEmployeeOut(BaseModel):
    id: int
    full_name: str
    model_config = {
        "from_attributes": True
    }

class UserEmployeeOut(BaseModel):
    id: int
    full_name: str
    model_config = {
        "from_attributes": True
    }

class EmployeeTaskOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    model_config = {
        "from_attributes": True
    }