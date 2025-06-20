from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientOut

router = APIRouter()

# Create new client
@router.post("/clients/", response_model=ClientOut)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.email == client.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Client already exists")
    new_client = Client(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

# Get all clients
@router.get("/clients/", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

# Get one client
@router.get("/clients/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Update client
@router.put("/clients/{client_id}", response_model=ClientOut)
def update_client(client_id: int, data: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in data.dict().items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client

# Delete client
@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    client.is_deleted = True
    db.commit()
    return {"message": "Client deleted successfully"}
