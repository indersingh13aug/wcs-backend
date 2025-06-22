# models.py
from sqlalchemy import Column, Integer, String, Text,Boolean,Float,DateTime
from app.database import Base
from datetime import datetime


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
