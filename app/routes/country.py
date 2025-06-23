from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.country import Country
from app.schemas.country import CountryOut

router = APIRouter()

@router.get("/countries", response_model=list[CountryOut])
def get_countries(db: Session = Depends(get_db)):
    return db.query(Country).all()
