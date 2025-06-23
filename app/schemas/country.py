from pydantic import BaseModel

class CountryBase(BaseModel):
    name: str
    code: str

class CountryOut(CountryBase):
    id: int

    model_config = {
        "from_attributes": True
    }

