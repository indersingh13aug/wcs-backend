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
    role_id: int | None = None
    service_id: int | None = None
    type_id: int | None = None
    contact_number: str | None = None
    contact_person: str | None = None
    date: date | None = None
    status: str | None = None

class SalesOut(SalesBase):
    id: int
    is_deleted: bool

    model_config = {
        "from_attributes": True
    }
    
