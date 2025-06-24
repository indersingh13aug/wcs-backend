from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    employee_id: int

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    username: str
    employee_name: str
    employee_id: Optional[int]  # ✅ required
    is_active: bool
    role_name: str   # ✅ Add this

    model_config = {
        "from_attributes": True
    }
