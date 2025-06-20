from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    email: str
    gst_number: str
    company: str

class ClientCreate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int
    model_config = {
        "from_attributes": True
    }
