from pydantic import BaseModel

class StateBase(BaseModel):
    name: str
    country_id: int


class StateOut(StateBase):
    id: int

    model_config = {
        "from_attributes": True
    }

