# schemas/project_employee_map.py
from pydantic import BaseModel
from datetime import date
from typing import List

class ProjectEmployeeMapBase(BaseModel):
    project_id: int
    employee_ids: List[int]  # Accept list of employees
    from_date: date
    to_date: date
    remarks: str

class ProjectEmployeeMapCreate(ProjectEmployeeMapBase):
    pass

class ProjectEmployeeMapOut(BaseModel):
    id: int
    project_id: int
    employee_id: int
    from_date: date
    to_date: date
    remarks: str
    is_deleted: bool

    model_config = {
        "from_attributes": True
    }
