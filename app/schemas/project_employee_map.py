# schemas/project_employee_map.py
from pydantic import BaseModel
from datetime import date
from typing import List
from typing import Optional

class ProjectEmployeeMapBase(BaseModel):
    project_id: int
    employee_ids: List[int]  
    from_date: date
    to_date: date
    remarks: Optional[str] = None

class ProjectEmployeeMapCreate(ProjectEmployeeMapBase):
    project_id: int
    employee_ids: List[int]  # 
    from_date: date
    to_date: date
    remarks: Optional[str] = None

class ProjectEmployeeMapUpdate(ProjectEmployeeMapBase):
    project_id: int
    employee_ids: List[int]  # ⬅️ multiple employee IDs
    from_date: date
    to_date: date
    remarks: Optional[str] = None

    

class RoleOut(BaseModel):
    name: Optional[str]

class EmployeeOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    role: Optional[RoleOut] = None
    ro_name: Optional[str] = None

class ProjectOut(BaseModel):
    id: int
    name: str

class ProjectEmployeeMapOut(BaseModel):
    id: int
    project: ProjectOut
    employee: EmployeeOut
    from_date: date
    to_date: date
    remarks: Optional[str]
    is_deleted: bool

    model_config = {
        "from_attributes": True
    }
