from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from app.db.models import Mascota
from app.schemas.mascota import MascotaCreate, MascotaUpdate, Mascota as MascotaSchema
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=MascotaSchema)
def create_mascota(mascota: MascotaCreate, x_auth_user_id: str = Header(None), db: Session = Depends(get_db)):
    if x_auth_user_id is None:
        raise HTTPException(status_code=400, detail="x_auth_user_id header is required")
    
    mascota_data = mascota.dict()
    mascota_data['id_usuario'] = int(x_auth_user_id)
    
    db_mascota = Mascota(**mascota_data)
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

@router.get("/", response_model=List[MascotaSchema])
def read_mascotas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    mascotas = db.query(Mascota).offset(skip).limit(limit).all()
    return mascotas

@router.get("/{mascota_id}", response_model=MascotaSchema)
def read_mascota(mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.query(Mascota).filter(Mascota.id_mascota == mascota_id).first()
    if mascota is None:
        raise HTTPException(status_code=404, detail="Mascota not found")
    return mascota

@router.put("/{mascota_id}", response_model=MascotaSchema)
def update_mascota(mascota_id: int, mascota: MascotaUpdate, db: Session = Depends(get_db)):
    db_mascota = db.query(Mascota).filter(Mascota.id_mascota == mascota_id).first()
    if db_mascota is None:
        raise HTTPException(status_code=404, detail="Mascota not found")
    for key, value in mascota.dict().items():
        setattr(db_mascota, key, value)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

@router.delete("/{mascota_id}", response_model=MascotaSchema)
def delete_mascota(mascota_id: int, db: Session = Depends(get_db)):
    db_mascota = db.query(Mascota).filter(Mascota.id_mascota == mascota_id).first()
    if db_mascota is None:
        raise HTTPException(status_code=404, detail="Mascota not found")
    db.delete(db_mascota)
    db.commit()
    return db_mascota

@router.get("/especie/{especie_id}", response_model=List[MascotaSchema])
def read_mascotas_by_especie(especie_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    mascotas = db.query(Mascota).filter(Mascota.id_especie == especie_id).offset(skip).limit(limit).all()
    return mascotas

@router.get("/raza/{raza_id}", response_model=List[MascotaSchema])
def read_mascotas_by_raza(raza_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    mascotas = db.query(Mascota).filter(Mascota.id_raza == raza_id).offset(skip).limit(limit).all()
    return mascotas