# app/schemas/project.py
from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    client_id: int


class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    client_id: int

    is_deleted: bool
    client_name: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
