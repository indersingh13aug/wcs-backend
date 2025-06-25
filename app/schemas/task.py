from pydantic import BaseModel

class TaskBase(BaseModel):
    name: str
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    is_deleted: bool

    model_config = {
        "from_attributes": True
    }

