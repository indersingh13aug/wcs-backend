from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate, RoleOut
from app.database import get_db

router = APIRouter()

@router.get("/roles", response_model=list[RoleOut])
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()

@router.post("/roles", response_model=RoleOut)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    existing = db.query(Role).filter(Role.name == role.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role with this name already exists")
    new = Role(**role.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.put("/roles/{role_id}", response_model=RoleOut)
def update_role(role_id: int, updated: RoleUpdate, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if db.query(Role).filter(Role.name == updated.name, Role.id != role_id).first():
        raise HTTPException(status_code=400, detail="Role with this name already exists")
    
    role.name = updated.name
    db.commit()
    db.refresh(role)
    return role

@router.put("/roles/{role_id}/activate")
def activate_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    role.is_deleted = False
    db.commit()
    return {"message": "Role activated"}

@router.put("/roles/{role_id}/deactivate")
def deactivate_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    role.is_deleted = True
    db.commit()
    return {"message": "Role deactivated"}
