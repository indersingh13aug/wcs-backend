from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.page import Page
from app.models.role_page_access import RolePageAccess
from app.schemas.page import PageCreate, PageOut
from app.schemas.access import AccessUpdate

router = APIRouter()

@router.get("/pages", response_model=list[PageOut])
def list_pages(db: Session = Depends(get_db)):
    return db.query(Page).all()

@router.post("/pages", response_model=PageOut)
def create_page(page: PageCreate, db: Session = Depends(get_db)):
    new_page = Page(**page.dict())
    db.add(new_page)
    db.commit()
    db.refresh(new_page)
    return new_page

@router.put("/access")
def update_access(access: AccessUpdate, db: Session = Depends(get_db)):
    db.query(RolePageAccess).filter_by(role_id=access.role_id).delete()
    for page_id in access.page_ids:
        db.add(RolePageAccess(role_id=access.role_id, page_id=page_id))
    db.commit()
    return {"status": "Access updated"}

@router.get("/access/{role_id}")
def get_access(role_id: int, db: Session = Depends(get_db)):
    accesses = db.query(RolePageAccess).filter_by(role_id=role_id).all()
    return [a.page_id for a in accesses]
