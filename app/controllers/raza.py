from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.models import Raza
from app.schemas.raza import RazaCreate, RazaUpdate, Raza as RazaSchema
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=RazaSchema)
def create_raza(raza: RazaCreate, db: Session = Depends(get_db)):
    db_raza = Raza(**raza.dict())
    db.add(db_raza)
    db.commit()
    db.refresh(db_raza)
    return db_raza

@router.get("/", response_model=List[RazaSchema])
def read_razas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    razas = db.query(Raza).offset(skip).limit(limit).all()
    return razas

@router.get("/{especie_id}", response_model=List[RazaSchema])
def read_razas_by_especie(especie_id: int, db: Session = Depends(get_db)):
    razas = db.query(Raza).filter(Raza.id_especie == especie_id).all()
    return razas

@router.get("/{raza_id}", response_model=RazaSchema)
def read_raza(raza_id: int, db: Session = Depends(get_db)):
    raza = db.query(Raza).filter(Raza.id_raza == raza_id).first()
    if raza is None:
        raise HTTPException(status_code=404, detail="Raza not found")
    return raza

@router.put("/{raza_id}", response_model=RazaSchema)
def update_raza(raza_id: int, raza: RazaUpdate, db: Session = Depends(get_db)):
    db_raza = db.query(Raza).filter(Raza.id_raza == raza_id).first()
    if db_raza is None:
        raise HTTPException(status_code=404, detail="Raza not found")
    for key, value in raza.dict().items():
        setattr(db_raza, key, value)
    db.commit()
    db.refresh(db_raza)
    return db_raza

@router.delete("/{raza_id}", response_model=RazaSchema)
def delete_raza(raza_id: int, db: Session = Depends(get_db)):
    db_raza = db.query(Raza).filter(Raza.id_raza == raza_id).first()
    if db_raza is None:
        raise HTTPException(status_code=404, detail="Raza not found")
    db.delete(db_raza)
    db.commit()
    return db_raza