from pydantic import BaseModel
from datetime import date
from typing import Optional
# from app.models.leave import LeaveStatus


class LeaveBase(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: Optional[str]
    type: str


class LeaveCreate(LeaveBase):
    pass


class LeaveUpdate(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    reason: Optional[str]
    type: Optional[str]
    status: Optional[str]


class LeaveOut(LeaveBase):
    id: int
    status: str

    model_config = {
        "from_attributes": True
    }
