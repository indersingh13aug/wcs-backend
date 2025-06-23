from pydantic import BaseModel

class ServiceBase(BaseModel):
    name: str

class ServiceCreate(ServiceBase):
    pass

class ServiceOut(ServiceBase):
    id: int

    model_config = {
        "from_attributes": True
    }

