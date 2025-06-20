from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    description: str
    client_id: int
    assigned_team: str  # comma-separated string

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    model_config = {
        "from_attributes": True
    }
