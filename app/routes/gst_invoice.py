# routes/gst_invoice.py
from fastapi import APIRouter, Response, Depends 
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.pdf_generator import generate_gst_invoice_pdf
from app.models.gst_invoice import GSTInvoice
from app.models.gst_item import GSTItems
from app.models.client import Client

router = APIRouter()

@router.get("/generate-receipt/{id}")
def generate_receipt(id: int, db: Session = Depends(get_db)):
    invoice = db.query(GSTInvoice).filter_by(id=id).first()
    items = db.query(GSTItems).filter_by(id=invoice.item_id).all()
    print('invoice.client_id')
    
    client = db.query(Client).filter_by(id=invoice.client_id).first()
    print(client.name)
    pdf = generate_gst_invoice_pdf(invoice, items, client,id)
    return Response(content=pdf, media_type="application/pdf")

@router.get("/invoices")
def list_invoices(db: Session = Depends(get_db)):
    invoices = db.query(GSTInvoice).all()
    for item in invoices:
        print(item.invoice_number)
        print(item.client_id)
        print(item.item_id)
        print(item.billing_date)

    return [
        {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "client_id": invoice.client_id,
            "item_id": invoice.item_id,
            "billing_date" : invoice.billing_date.isoformat()
        }
        for invoice in invoices
    ]
