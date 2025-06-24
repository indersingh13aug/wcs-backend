from pydantic import BaseModel
from typing import Optional

class PageBase(BaseModel):
    name: str
    path: str
    group_name: str

class PageCreate(PageBase):
    pass

class PageOut(BaseModel):
    id: int
    name: str
    path: str
    group_name: Optional[str] = None
    is_deleted: bool

    model_config = {
        "from_attributes": True
    }
