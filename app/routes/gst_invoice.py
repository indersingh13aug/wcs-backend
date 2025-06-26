# routes/gst_invoice.py
from fastapi import APIRouter, Response, Depends ,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.pdf_generator import generate_gst_invoice_pdf
from app.models.gst_invoice import GSTInvoice, GSTInvoiceItem
from app.models.client import Client
from app.schemas.gst_invoice import GSTInvoiceCreate, GSTInvoiceOut, GSTInvoiceItemCreate
from datetime import datetime
from sqlalchemy.orm import joinedload


router = APIRouter()


def generate_invoice_number(db):
    last_invoice = db.query(GSTInvoice).order_by(GSTInvoice.id.desc()).first()
    if not last_invoice:
        return "INV-1001"
    last_num = int(last_invoice.invoice_number.split("-")[1])
    return f"INV-{last_num + 1}"



@router.post("/invoices")
def create_gst_invoice(data: GSTInvoiceCreate, db: Session = Depends(get_db)):
    try:
        # Auto-generate invoice number (e.g., "INV20250626001")
        latest_invoice = db.query(GSTInvoice).order_by(GSTInvoice.id.desc()).first()
        next_id = latest_invoice.id + 1 if latest_invoice else 1
        today_str = datetime.today().strftime("%Y%m%d")
        invoice_number = f"INV{today_str}{str(next_id).zfill(3)}"

        # Calculate total invoice amount
        total = sum(item.total_amount for item in data.items)

        invoice = GSTInvoice(
            invoice_number=invoice_number,
            client_id=data.client_id,
            billing_date=data.billing_date,
            total_amount=total
        )

        db.add(invoice)
        db.flush()  # Needed to get invoice.id before inserting related items

        # Add invoice items
        for item in data.items:
            db_item = GSTInvoiceItem(
                invoice_id=invoice.id,
                item_id=item.item_id,
                quantity=item.quantity,
                rate_per_unit=item.rate_per_unit,
                cgst_amount=item.cgst_amount,
                sgst_amount=item.sgst_amount,
                igst_amount=item.igst_amount,
                total_amount=item.total_amount
            )
            db.add(db_item)

        db.commit()
        return {"message": "Invoice created successfully", "invoice_number": invoice_number}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/invoices/{invoice_id}/pdf", response_class=Response)
def generate_invoice_pdf(invoice_id: int, db: Session = Depends(get_db)):
    invoice = (
        db.query(GSTInvoice)
        .filter(GSTInvoice.id == invoice_id, GSTInvoice.is_deleted == False)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    client = invoice.client

    # ❗ Filter out deleted items
    items = [i for i in invoice.items if not i.is_deleted]

    if not items:
        raise HTTPException(status_code=400, detail="No active items in this invoice")

    # Prepare invoice data
    invoice_dict = {
        "invoice_number": invoice.invoice_number,
        "billing_date": invoice.billing_date,
        "total_amount": invoice.total_amount,
        "cgst_amount": sum(i.cgst_amount for i in items),
        "sgst_amount": sum(i.sgst_amount for i in items),
        "igst_amount": sum(i.igst_amount for i in items),
    }

    item_dicts = [
        {
            "item_name": i.item.item_name,
            "hsn_sac": i.item.hsn_sac,
            "rate_per_unit": i.rate_per_unit,
            "quantity": i.quantity,
            "cgst_rate": i.item.cgst_rate,
            "sgst_rate": i.item.sgst_rate,
            "igst_rate": i.item.igst_rate,
            "cgst_amount": i.cgst_amount,
            "sgst_amount": i.sgst_amount,
            "igst_amount": i.igst_amount,
            "total_amount": i.total_amount,
        }
        for i in items
    ]

    client_dict = {
        "name": client.name,
        "phone": client.phone,
        "address": ", ".join(filter(None, [
            client.addressline1,
            client.addressline2,
            client.state,
            client.country,
            client.pincode
        ]))
    }

    # Generate PDF
    pdf = generate_gst_invoice_pdf(invoice_dict, item_dicts, client_dict, id=invoice_id)

    # Return PDF response
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=invoice_{invoice.invoice_number}.pdf"}
    )


@router.put("/invoice-items/{item_id}/delete")
def soft_delete_invoice_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(GSTInvoiceItem).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.is_deleted = True
    db.commit()

    # Check if all items in this invoice are deleted
    remaining_items = db.query(GSTInvoiceItem).filter(
        GSTInvoiceItem.invoice_id == item.invoice_id,
        GSTInvoiceItem.is_deleted == False
    ).count()

    if remaining_items == 0:
        # Soft delete the invoice as well
        invoice = db.query(GSTInvoice).filter_by(id=item.invoice_id).first()
        if invoice:
            invoice.is_deleted = True
            db.commit()

    return {"message": "Item deleted"}


# @router.get("/generate-receipt/{id}")
# def generate_receipt(id: int, db: Session = Depends(get_db)):
#     invoice = db.query(GSTInvoice).filter_by(id=id).first()
#     items = db.query(GSTInvoiceItem).filter_by(id=invoice.item_id).all()
#     print('invoice.client_id')
    
#     client = db.query(Client).filter_by(id=invoice.client_id).first()
#     print(client.name)
#     pdf = generate_gst_invoice_pdf(invoice, items, client,id)
#     return Response(content=pdf, media_type="application/pdf")

# @router.get("/gst-invoices", response_model=list[GSTInvoiceOut])
# def get_all_invoices(db: Session = Depends(get_db)):
#     invoices = db.query(GSTInvoice).filter_by(is_deleted=False).all()
#     return invoices

@router.get("/gst-invoices", response_model=list[GSTInvoiceOut])
def get_all_invoices(db: Session = Depends(get_db)):
    invoices = (
        db.query(GSTInvoice)
        .filter(GSTInvoice.is_deleted == False)
        .options(joinedload(GSTInvoice.items).joinedload(GSTInvoiceItem.item))
        .all()
    )

    # Filter deleted invoice items before returning
    for invoice in invoices:
        invoice.items = [item for item in invoice.items if not item.is_deleted]

    return invoices

@router.patch("/invoices/{invoice_id}/delete")
def soft_delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(GSTInvoice).filter(GSTInvoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice.is_deleted = True
    db.commit()
    return {"message": "Invoice deleted"}

@router.get("/invoices")
def list_invoices(db: Session = Depends(get_db)):
    invoices = db.query(GSTInvoice).all()

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
