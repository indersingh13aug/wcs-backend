from pydantic import BaseModel, EmailStr
from typing import Optional

class ClientBase(BaseModel):
    name: str
    contact_person: Optional[str]
    email: EmailStr
    phone: Optional[str]
    address: Optional[str]
    gst_number: Optional[str]

class ClientCreate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int

    model_config = {
        "from_attributes": True
    }
