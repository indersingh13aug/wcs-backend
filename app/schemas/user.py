from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    employee_id: int

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    is_active: bool
    employee_name: str

    model_config = {
        "from_attributes": True
    }
