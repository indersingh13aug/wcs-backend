# models.py
from sqlalchemy import Column, Integer, String, Text, Date,Boolean,Float, ForeignKey,DateTime
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from datetime import date

class GSTItems(Base):
    __tablename__ = "gst_items"
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    hsn_sac = Column(String, nullable=False)
    cgst_rate = Column(Float, nullable=False, default=0.0)
    sgst_rate = Column(Float, nullable=False, default=0.0)
    igst_rate = Column(Float, nullable=False, default=0.0)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Optional: backref for reverse relationship if needed
    invoice_items = relationship("GSTInvoiceItem", back_populates="item")
    

class GSTInvoice(Base):
    __tablename__ = "gst_invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, nullable=False, unique=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    billing_date = Column(Date, nullable=False, default=date.today)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    client = relationship("Client", backref="invoices")
    items = relationship("GSTInvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class GSTInvoiceItem(Base):
    __tablename__ = "gst_invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("gst_invoices.id"))
    item_id = Column(Integer, ForeignKey("gst_items.id"))

    quantity = Column(Integer, nullable=False)
    rate_per_unit = Column(Float, nullable=False)

    cgst_amount = Column(Float, nullable=False)
    sgst_amount = Column(Float, nullable=False)
    igst_amount = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    is_deleted = Column(Boolean, default=False)
    invoice = relationship("GSTInvoice", back_populates="items")
    item = relationship("GSTItems")