from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.page import Page
from app.schemas.page import PageCreate, PageOut
from app.schemas.access import AccessUpdate

router = APIRouter()

@router.get("/admin/pages", response_model=list[PageOut])
def list_pages(db: Session = Depends(get_db)):
    return db.query(Page).all()

@router.post("/admin/pages", response_model=PageOut)
def create_page(page: PageCreate, db: Session = Depends(get_db)):
    new_page = Page(**page.dict())
    db.add(new_page)
    db.commit()
    db.refresh(new_page)
    return new_page


@router.put("/admin/pages/{page_id}", response_model=PageOut)
def update_page(page_id: int, updated: PageCreate, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    # Check for duplicate name (excluding the current page)
    duplicate = db.query(Page).filter(
        Page.name == updated.name,
        Page.id != page_id
    ).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Page with this name already exists")

    # Update fields
    for key, value in updated.dict().items():
        setattr(page, key, value)

    db.commit()
    db.refresh(page)
    return page

@router.put("/admin/pages/{page_id}/activate")
def activate_page(page_id: int, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    page.is_deleted = False
    db.commit()
    db.refresh(page)
    return {"message": "Page activated successfully", "page": page}

@router.put("/admin/pages/{page_id}/deactivate")
def deactivate_page(page_id: int, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    page.is_deleted = True
    db.commit()
    db.refresh(page)
    return {"message": "Page deactivated successfully", "page": page}

