from pydantic import BaseModel
from datetime import date

class SalesBase(BaseModel):
    client_id: int
    role_id: int
    service_id: int
    type_id: int
    contact_number: str
    contact_person: str
    date: date
    status: str  # "lead", "opportunity", "active"

class SalesCreate(SalesBase):
    pass

class SalesUpdate(BaseModel):
    client_id: int
    role_id: int
    service_id: int
    type_id: int
    contact_number: str
    contact_person: str
    date: date
    status: str 

class SalesOut(SalesBase):
    id: int
    client_id: int
    client_name: str
    role_id: int
    role_name: str
    service_id: int
    service_name: str
    type_id: int
    type_name: str
    contact_person: str
    contact_number: str
    date: date
    status: str
    is_deleted: bool
    
    model_config = {
        "from_attributes": True
    }
    
