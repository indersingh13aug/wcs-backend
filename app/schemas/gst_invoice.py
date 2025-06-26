from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional


# -------------------------------
# Client Response Model (For Out)
# -------------------------------
class ClientOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


# -------------------------------
# GST Item Schemas
# -------------------------------
class GSTItemBase(BaseModel):
    item_name: str = Field(..., example="Consulting Services")
    description: Optional[str] = Field(None, example="Professional consulting services")
    hsn_sac: str = Field(..., min_length=1, max_length=8, example="99831231")
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


# -------------------------------
# Invoice Item Schemas
# -------------------------------
class GSTInvoiceItemCreate(BaseModel):
    item_id: int
    quantity: int
    rate_per_unit: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    total_amount: float


class GSTInvoiceItemOut(BaseModel):
    id: int                   
    item_id: int
    quantity: int
    rate_per_unit: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    total_amount: float
    item: GSTItemOut

    model_config = {
        "from_attributes": True
    }


# -------------------------------
# Invoice Schemas
# -------------------------------
class GSTInvoiceCreate(BaseModel):
    client_id: int
    billing_date: date
    items: List[GSTInvoiceItemCreate]


class GSTInvoiceOut(BaseModel):
    id: int
    invoice_number: str 
    client: ClientOut
    items: List[GSTInvoiceItemOut]

    model_config = {
        "from_attributes": True
    }

