from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from  app.schemas.gst_invoice import GSTItemCreate, GSTItemUpdate, GSTItemOut
from app.crud import gst_item as crud
from app.database import get_db
from app.models.gst_invoice import GSTItems 
from typing import List

router = APIRouter()


@router.get("/gst-items", response_model=List[GSTItemOut])
def get_all_items(db: Session = Depends(get_db)):
    return crud.get_all_items(db)


@router.get("/gst-items/active", response_model=List[GSTItemOut])
def get_active_items(db: Session = Depends(get_db)):
    return crud.get_active_items(db)


@router.get("/gst-items/{item_id}", response_model=GSTItemOut)
def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="GST Item not found")
    return item


@router.post("/gst-items", response_model=GSTItemOut)
def create_item(item: GSTItemCreate, db: Session = Depends(get_db)):
    existing = db.query(GSTItems).filter(GSTItems.item_name == item.item_name, GSTItems.is_deleted == False).first()
    if existing:
        raise HTTPException(status_code=400, detail="GST Item with this name already exists")
    
    db_item = GSTItems(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



@router.put("/gst-items/{item_id}", response_model=GSTItemOut)
def update_item(item_id: int, updated: GSTItemUpdate, db: Session = Depends(get_db)):
    item = db.query(GSTItems).filter(GSTItems.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if another item (not itself) has the same name
    duplicate = db.query(GSTItems).filter(
        GSTItems.item_name == updated.item_name,
        GSTItems.id != item_id,
        GSTItems.is_deleted == False
    ).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="GST Item with this name already exists")
    
    for key, value in updated.dict().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

