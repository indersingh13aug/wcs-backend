# models.py
from sqlalchemy import Column, Integer, String, Text, Date,Boolean,Float, ForeignKey,DateTime
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class GSTInvoice(Base):
    __tablename__ = "gst_invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, nullable=False, unique=True)

    item_id = Column(Integer, ForeignKey("gst_items.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False) 

    quantity = Column(Integer, nullable=False)
    rate_per_unit = Column(Float, nullable=False)

    cgst_amount = Column(Float, nullable=False)
    sgst_amount = Column(Float, nullable=False)
    igst_amount = Column(Float, nullable=False)

    total_amount = Column(Float, nullable=False)
    billing_date = Column(Date, nullable=False)

    # Relationships
    item = relationship("GSTItems", backref="invoices")
    client = relationship("Client", backref="invoices") 




