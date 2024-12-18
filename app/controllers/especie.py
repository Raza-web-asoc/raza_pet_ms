from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.models import Especie
from app.schemas.especie import EspecieCreate, EspecieUpdate, Especie as EspecieSchema
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=EspecieSchema)
def create_especie(especie: EspecieCreate, db: Session = Depends(get_db)):
    db_especie = Especie(nombre_especie=especie.nombre_especie)
    db.add(db_especie)
    db.commit()
    db.refresh(db_especie)
    return db_especie

@router.get("/", response_model=List[EspecieSchema])
def read_especies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    especies = db.query(Especie).offset(skip).limit(limit).all()
    return especies

@router.get("/{especie_id}", response_model=EspecieSchema)
def read_especie(especie_id: int, db: Session = Depends(get_db)):
    especie = db.query(Especie).filter(Especie.id_especie == especie_id).first()
    if especie is None:
        raise HTTPException(status_code=404, detail="Especie not found")
    return especie

@router.put("/{especie_id}", response_model=EspecieSchema)
def update_especie(especie_id: int, especie: EspecieUpdate, db: Session = Depends(get_db)):
    db_especie = db.query(Especie).filter(Especie.id_especie == especie_id).first()
    if db_especie is None:
        raise HTTPException(status_code=404, detail="Especie not found")
    for key, value in especie.dict().items():
        setattr(db_especie, key, value)
    db.commit()
    db.refresh(db_especie)
    return db_especie

@router.delete("/{especie_id}", response_model=EspecieSchema)
def delete_especie(especie_id: int, db: Session = Depends(get_db)):
    db_especie = db.query(Especie).filter(Especie.id_especie == especie_id).first()
    if db_especie is None:
        raise HTTPException(status_code=404, detail="Especie not found")
    db.delete(db_especie)
    db.commit()
    return db_especie