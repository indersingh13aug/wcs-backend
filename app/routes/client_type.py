from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.client_type import ClientType
from app.schemas.client_type import ClientTypeCreate, ClientTypeOut
from app.database import get_db

router = APIRouter()

@router.get("/client-types", response_model=list[ClientTypeOut])
def get_types(db: Session = Depends(get_db)):
    return db.query(ClientType).all()

@router.post("/client-types", response_model=ClientTypeOut)
def create_type(data: ClientTypeCreate, db: Session = Depends(get_db)):
    if db.query(ClientType).filter_by(type_name=data.type_name).first():
        raise HTTPException(400, detail="Client type already exists")
    new_type = ClientType(**data.dict())
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type
