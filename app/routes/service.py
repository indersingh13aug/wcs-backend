from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceOut,ServiceUpdate
from app.database import get_db

router = APIRouter()

@router.get("/services", response_model=list[ServiceOut])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()

@router.post("/services", response_model=ServiceOut)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    if db.query(Service).filter_by(name=service.name).first():
        raise HTTPException(400, detail="Service already exists")
    new_service = Service(**service.dict())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service



@router.put("/services/{service_id}", response_model=ServiceOut)
def update_service(service_id: int, updated: ServiceUpdate, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if db.query(Service).filter(Service.name == updated.name, Service.id != service_id).first():
        raise HTTPException(status_code=400, detail="Service with this name already exists")
    
    service.name = updated.name
    db.commit()
    db.refresh(service)
    return service

@router.put("/services/{service_id}/activate")
def activate_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    service.is_deleted = False
    db.commit()
    return {"message": "Service activated"}

@router.put("/services/{service_id}/deactivate")
def deactivate_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    service.is_deleted = True
    db.commit()
    return {"message": "Service deactivated"}
