from pydantic import BaseModel
from typing import Optional

class LeaveTypeBase(BaseModel):
    name: str
    max_days: int
    description: Optional[str]

class LeaveTypeCreate(LeaveTypeBase):
    pass

class LeaveTypeUpdate(LeaveTypeBase):
    pass

class LeaveTypeOut(LeaveTypeBase):
    id: int
    is_deleted: bool

    model_config = {
        "from_attributes": True
    }
