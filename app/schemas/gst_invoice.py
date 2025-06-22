from pydantic import BaseModel, Field
from datetime import date

class GSTInvoiceBase(BaseModel):
    invoice_number: str
    item_id: int
    client_id: int
    quantity: int
    rate_per_unit: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    total_amount: float
    billing_date: date

class GSTInvoiceCreate(GSTInvoiceBase):
    pass

class GSTInvoiceUpdate(GSTInvoiceBase):
    pass

class GSTInvoiceOut(GSTInvoiceBase):
    id: int
    model_config = {
        "from_attributes": True
    }
