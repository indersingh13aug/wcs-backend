from sqlalchemy.orm import Session
from app.models.gst_item import GSTItems
from app.schemas.gst_item import GSTItemCreate, GSTItemUpdate

def get_all_items(db: Session):
    return db.query(GSTItems).all()

def get_active_items(db: Session):
    return db.query(GSTItems).filter(GSTItems.is_active == True).all()

def get_item_by_id(db: Session, item_id: int):
    return db.query(GSTItems).filter(GSTItems.id == item_id).first()

def create_item(db: Session, item: GSTItemCreate):
    new_item = GSTItems(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def update_item(db: Session, item_id: int, item_data: GSTItemUpdate):
    db_item = db.query(GSTItems).filter(GSTItems.id == item_id).first()
    if not db_item:
        return None

    for field, value in item_data.dict(exclude_unset=True).items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item
