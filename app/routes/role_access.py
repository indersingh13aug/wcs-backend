from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.role_page_access import RolePageAccess
from app.models.page import Page
from app.schemas.role_access import PageCreate, PageOut, AccessAssign

router = APIRouter()

@router.get("/admin/pages", response_model=list[PageOut])
def get_pages(db: Session = Depends(get_db)):
    return db.query(Page).all()


@router.get("/admin/accessible")
def get_accessible_pages(role_id: int, db: Session = Depends(get_db)):
    accesses = db.query(RolePageAccess).filter_by(role_id=role_id).all()
    page_ids = [a.page_id for a in accesses]

    pages = db.query(Page).filter(Page.id.in_(page_ids), Page.is_deleted == False).all()
    return [{"name": p.name, "path": p.path, "group_name": p.group_name or "Other"} for p in pages]

@router.get("/admin/access/{role_id}")
def get_access(role_id: int, db: Session = Depends(get_db)):
    accesses = db.query(RolePageAccess).filter_by(role_id=role_id).all()
    return [a.page_id for a in accesses]


@router.post("/admin/pages")
def add_page(payload: PageCreate, db: Session = Depends(get_db)):
    page = Page(**payload.dict())
    db.add(page)
    db.commit()
    db.refresh(page)
    return {"msg": "Page created", "page": page}

@router.put("/admin/access")
def assign_access(payload: AccessAssign, db: Session = Depends(get_db)):
    db.query(RolePageAccess).filter_by(role_id=payload.role_id).delete()
    for page_id in payload.page_ids:
        db.add(RolePageAccess(role_id=payload.role_id, page_id=page_id))
    db.commit()
    return {"msg": "Access updated"}
