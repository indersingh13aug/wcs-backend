from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Sales, Client, Role, Service, ClientType
from app.schemas.sales import SalesCreate, SalesUpdate, SalesOut

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("/", response_model=List[SalesOut])
def get_sales(include_deleted: bool = False, db: Session = Depends(get_db)):
    query = db.query(
        Sales.id,
        Sales.client_id,
        Client.name.label("client_name"),
        Sales.role_id,
        Role.name.label("role_name"),
        Sales.service_id,
        Service.name.label("service_name"),
        Sales.type_id,
        ClientType.type_name.label("type_name"),
        Sales.contact_person,
        Sales.contact_number,
        Sales.date,
        Sales.status,
        Sales.is_deleted
    ).join(Client, Client.id == Sales.client_id
    ).join(Role, Role.id == Sales.role_id
    ).join(Service, Service.id == Sales.service_id
    ).join(ClientType, ClientType.id == Sales.type_id)

    # if not include_deleted:
    #     query = query.filter(Sales.is_deleted == False)

    return query.all()


@router.post("/", response_model=SalesOut)
def create_sale(payload: SalesCreate, db: Session = Depends(get_db)):
    sale = Sales(**payload.dict())
    db.add(sale)
    db.commit()
    db.refresh(sale)

    # Join to return names
    return db.query(
        Sales.id,
        Sales.client_id,
        Client.name.label("client_name"),
        Sales.role_id,
        Role.name.label("role_name"),
        Sales.service_id,
        Service.name.label("service_name"),
        Sales.type_id,
        ClientType.type_name.label("type_name"),
        Sales.contact_person,
        Sales.contact_number,
        Sales.date,
        Sales.status,
        Sales.is_deleted
    ).join(Client).join(Role).join(Service).join(ClientType).filter(Sales.id == sale.id).first()


@router.put("/{id}", response_model=SalesOut)
def update_sale(id: int, payload: SalesUpdate, db: Session = Depends(get_db)):
    sale = db.query(Sales).filter(Sales.id == id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    for field, value in payload.dict().items():
        setattr(sale, field, value)

    db.commit()

    return db.query(
        Sales.id,
        Sales.client_id,
        Client.name.label("client_name"),
        Sales.role_id,
        Role.name.label("role_name"),
        Sales.service_id,
        Service.name.label("service_name"),
        Sales.type_id,
        ClientType.type_name.label("type_name"),
        Sales.contact_person,
        Sales.contact_number,
        Sales.date,
        Sales.status,
        Sales.is_deleted
    ).join(Client).join(Role).join(Service).join(ClientType).filter(Sales.id == id).first()


@router.put("/{id}/activate")
def activate_sale(id: int, db: Session = Depends(get_db)):
    sale = db.query(Sales).filter(Sales.id == id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    sale.is_deleted = False
    db.commit()
    return {"message": "Sale activated"}


@router.put("/{id}/deactivate")
def deactivate_sale(id: int, db: Session = Depends(get_db)):
    sale = db.query(Sales).filter(Sales.id == id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    sale.is_deleted = True
    db.commit()
    return {"message": "Sale deactivated"}
