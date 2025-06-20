# models.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class GSTInvoice(Base):
    __tablename__ = "gst_invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    date = Column(Date)
    company_name = Column(String)
    company_gstin = Column(String)
    client_name = Column(String)
    client_gstin = Column(String)
    total_amount = Column(Float)
    cgst = Column(Float)
    sgst = Column(Float)
    igst = Column(Float)
    final_amount = Column(Float)

    items = relationship("GSTInvoiceItem", back_populates="invoice")

class GSTInvoiceItem(Base):
    __tablename__ = "gst_invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("gst_invoices.id"))
    description = Column(String)
    hsn_sac = Column(String)
    quantity = Column(Integer)
    rate = Column(Float)
    amount = Column(Float)

    invoice = relationship("GSTInvoice", back_populates="items")
