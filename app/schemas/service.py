from pydantic import BaseModel

class ServiceBase(BaseModel):
    name: str

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class ServiceOut(ServiceBase):
    id: int
    is_deleted: bool
    model_config = {
        "from_attributes": True
    }

