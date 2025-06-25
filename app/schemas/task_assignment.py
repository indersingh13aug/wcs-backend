from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional


class ProjectOut(BaseModel):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }

class TaskOut(BaseModel):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }

class EmployeeOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    model_config = {
        "from_attributes": True
    }

class TaskAssignmentBase(BaseModel):
    project_id: int
    task_id: int
    employee_id: int
    start_date: date
    end_date: date

class TaskAssignmentCreate(TaskAssignmentBase):
    pass

class TaskAssignmentOut(BaseModel):
    id: int
    start_date: date
    end_date: date
    project: ProjectOut
    task: TaskOut
    employee: EmployeeOut
    # comments: Optional[List[str]] = []  
    model_config = {
        "from_attributes": True
    }


class TaskCommentCreate(BaseModel):
    assignment_id: int
    employee_id: int
    comment: str

class CommentOut(BaseModel):
    id: int
    text: str
    created_at: datetime
    employee_id: str

    model_config = {
        "from_attributes": True
    }


class TaskCommentOut(BaseModel):
    id: int
    comment: str
    timestamp: datetime
    employee_name: str

    model_config = {
        "from_attributes": True
    }

