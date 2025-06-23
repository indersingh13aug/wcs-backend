from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceOut
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
