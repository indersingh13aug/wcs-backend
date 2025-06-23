from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.state import State
from app.models.country import Country
from app.schemas.state import StateOut

router = APIRouter()


@router.get("/states", response_model=list[StateOut])
def get_states_by_country(country_id: int = Query(None),country_code: str = Query(None),db: Session = Depends(get_db)):
    if not country_id and not country_code:
        raise HTTPException(status_code=400, detail="Provide either country_id or country_code")

    if country_code:
        country = db.query(Country).filter_by(code=country_code.upper()).first()
        if not country:
            raise HTTPException(status_code=404, detail="Country not found by code")
        country_id = country.id

    states = db.query(State).filter_by(country_id=country_id).all()
    return states
