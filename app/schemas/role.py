from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: int
    is_deleted: bool

    model_config = {
        "from_attributes": True
    }
