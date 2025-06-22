from pydantic import BaseModel, Field
from typing import Optional

class GSTItemBase(BaseModel):
    item_name: str = Field(..., example="Consulting Services")
    description: Optional[str] = Field(None, example="Professional consulting services")
    hsn_sac: str = Field(..., min_length=0, max_length=8, example="998311")
    cgst_rate: float = Field(..., example=9.0)
    sgst_rate: float = Field(..., example=9.0)
    igst_rate: float = Field(..., example=18.0)

class GSTItemCreate(GSTItemBase):
    pass

class GSTItemUpdate(GSTItemBase):
    pass

class GSTItemOut(GSTItemBase):
    id: int

    model_config = {
        "from_attributes": True
    }
