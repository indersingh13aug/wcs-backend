# routes/gst_receipt.py
from fastapi import APIRouter, Response, Depends 
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.pdf_generator import generate_gst_receipt_pdf
from app.models import GSTInvoice, GSTInvoiceItem

router = APIRouter()

@router.get("/generate-receipt/{invoice_id}")
def generate_receipt(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(GSTInvoice).filter_by(id=invoice_id).first()
    items = db.query(GSTInvoiceItem).filter_by(invoice_id=invoice_id).all()
    pdf = generate_gst_receipt_pdf(invoice, items)
    return Response(content=pdf, media_type="application/pdf")

@router.get("/invoices")
def list_invoices(db: Session = Depends(get_db)):
    invoices = db.query(GSTInvoice).all()
    return [
        {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "client_name": invoice.client_name,
            "date": invoice.date.isoformat()
        }
        for invoice in invoices
    ]
