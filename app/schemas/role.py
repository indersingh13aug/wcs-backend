from pydantic import BaseModel

class RoleOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }
