from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleOut  # create if not available
from app.database import get_db

router = APIRouter()

@router.get("/roles", response_model=list[RoleOut])
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()
