from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.sales import Sales
from app.schemas.sales import SalesCreate, SalesUpdate, SalesOut
from app.database import get_db

router = APIRouter()

@router.get("/sales", response_model=list[SalesOut])
def get_sales(db: Session = Depends(get_db)):
    return db.query(Sales).filter_by(is_deleted=False).all()

@router.post("/sales", response_model=SalesOut)
def create_sale(data: SalesCreate, db: Session = Depends(get_db)):
    new = Sales(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.put("/sales/{sale_id}", response_model=SalesOut)
def update_sale(sale_id: int, data: SalesUpdate, db: Session = Depends(get_db)):
    sale = db.query(Sales).filter_by(id=sale_id).first()
    if not sale:
        raise HTTPException(404, detail="Sale not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(sale, field, value)
    db.commit()
    db.refresh(sale)
    return sale

@router.put("/sales/{sale_id}/delete")
def soft_delete_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sales).filter_by(id=sale_id).first()
    if not sale:
        raise HTTPException(404, detail="Sale not found")
    sale.is_deleted = True
    db.commit()
    return {"message": "Sale deleted"}

@router.put("/sales/{sale_id}/status/{new_status}")
def update_status(sale_id: int, new_status: str, db: Session = Depends(get_db)):
    if new_status not in ["lead", "opportunity", "active"]:
        raise HTTPException(400, detail="Invalid status")
    sale = db.query(Sales).filter_by(id=sale_id).first()
    if not sale:
        raise HTTPException(404, detail="Sale not found")
    sale.status = new_status
    db.commit()
    return {"message": f"Status updated to {new_status}"}
