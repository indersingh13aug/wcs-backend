from pydantic import BaseModel
from typing import List

class RoleUserAssign(BaseModel):
    role_id: int
    employee_ids: List[int]

class RoleUserOut(BaseModel):
    role_id: int
    employee_id: int
