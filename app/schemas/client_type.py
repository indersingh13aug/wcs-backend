from pydantic import BaseModel

class ClientTypeBase(BaseModel):
    type_name: str

class ClientTypeCreate(ClientTypeBase):
    pass

class ClientTypeOut(ClientTypeBase):
    id: int

    model_config = {
        "from_attributes": True
    }
