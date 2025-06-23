from pydantic import BaseModel

class PageBase(BaseModel):
    name: str
    path: str

class PageCreate(PageBase):
    pass

class PageOut(PageBase):
    id: int

    model_config = {
        "from_attributes": True
    }
