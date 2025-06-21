from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientOut
from app.database import get_db

router = APIRouter()

# Create a new client
@router.post("/clients", response_model=ClientOut)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.email == client.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Client with this email already exists")
    new_client = Client(**client.model_dump())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

# Get all clients (paginated)
@router.get("/clients", response_model=list[ClientOut])
def get_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Client).offset(skip).limit(limit).all()

@router.put("/clients/{client_id}/activate")
def activate_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client.is_deleted = False
    db.commit()
    db.refresh(client)
    return {"message": "Client activated successfully", "client": client}

@router.put("/clients/{client_id}/deactivate")
def deactivate_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client.is_deleted = True
    db.commit()
    db.refresh(client)
    return {"message": "Client deactivated successfully", "client": client}


# Get single client
@router.get("/clients/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Update client
@router.put("/clients/{client_id}", response_model=ClientOut)
def update_client(client_id: int, updated: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check for duplicate name (excluding the current client)
    duplicate = db.query(Client).filter(
        Client.name == updated.name,
        Client.id != client_id
    ).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Client with this name already exists")

    # Update fields
    for key, value in updated.dict().items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client

# Soft delete client
@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    client.is_deleted = True
    db.commit()
    return {"message": "Client soft-deleted successfully"}
