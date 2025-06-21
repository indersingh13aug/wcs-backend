# app/schemas/project.py
from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    client_id: int
    assigned_team: Optional[str] = ""

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    client_id: int
    assigned_team: Optional[str]  # comma-separated ids
    is_deleted: bool
    client_name: Optional[str] = None
    assigned_team_names: Optional[list[str]] = None  # <- Add this

    model_config = {
        "from_attributes": True
    }
