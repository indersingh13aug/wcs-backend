from pydantic import BaseModel, EmailStr
from typing import Optional

class ClientBase(BaseModel):
    name: str
    contact_person: Optional[str]
    client_code: Optional[str]
    email: EmailStr
    phone: Optional[str]
    address: Optional[str]
    gst_number: Optional[str]

class ClientCreate(ClientBase):
    pass

# 🔹 For Updating a Client
class ClientUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    client_code: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    gst_number: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class ClientOut(ClientBase):
    id: int
    is_deleted: bool
    model_config = {
        "from_attributes": True
    }
