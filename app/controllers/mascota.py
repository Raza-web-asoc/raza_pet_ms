from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from app.db.models import Mascota, Especie, Raza
from app.schemas.mascota import MascotaCreate, MascotaUpdate,MascotaInDBBase,  Mascota as MascotaSchema
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=MascotaInDBBase)
def create_mascota(mascota: MascotaCreate, x_auth_user_id: str = Header(None), db: Session = Depends(get_db)):
    if x_auth_user_id is None:
        raise HTTPException(status_code=400, detail="x_auth_user_id header is required")

    # Añadir el id_usuario desde el header
    mascota_data = mascota.dict()
    mascota_data['id_usuario'] = int(x_auth_user_id)

    # Crear la nueva mascota en la base de datos
    db_mascota = Mascota(**mascota_data)
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

@router.get("/", response_model=List[MascotaSchema])
def read_mascotas(db: Session = Depends(get_db)):

    mascotas = (
        db.query(
            Mascota,
            Especie.nombre_especie,
            Raza.nombre_raza,
            Raza.id_especie,
        )
        .join(Raza, Mascota.id_raza == Raza.id_raza)
        .all()
    )

    result = [
        {
            **mascota.__dict__,
            'id_especie': id_especie,
            'nombre_especie': nombre_especie,
            'nombre_raza': nombre_raza
        }
        for mascota, nombre_especie, nombre_raza, id_especie in mascotas
    ]

    return result

@router.get("/especie/{especie_id}/usuario/{usuario_id}", response_model=List[MascotaSchema])
def read_mascotas_by_especie_not_user(especie_id: int, usuario_id: int, db: Session = Depends(get_db)):
    # Realizamos un join entre las tablas Mascota, Raza y Especie
    mascotas = (
        db.query(
            Mascota,
            Especie.nombre_especie,
            Raza.nombre_raza,
            Raza.id_especie
        )
        .join(Raza, Mascota.id_raza == Raza.id_raza)  # Unimos Mascota con Raza
        .join(Especie, Raza.id_especie == Especie.id_especie)  # Unimos Raza con Especie
        .filter(Especie.id_especie == especie_id)  # Filtro por especie
        .filter(Mascota.id_usuario != usuario_id)  # Filtro para excluir las mascotas del usuario
        .all()
    )

    # Preparamos el resultado con los campos de la mascota junto con el nombre de especie y raza
    result = [
        {
            **mascota.__dict__,
            'id_especie': id_especie,
            'nombre_especie': nombre_especie,
            'nombre_raza': nombre_raza
        }
        for mascota, nombre_especie, nombre_raza, id_especie in mascotas
    ]

    return result




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

@router.get("/usuario/{usuario_id}", response_model=List[MascotaSchema])
def read_mascotas_by_usuario(usuario_id: int, db: Session = Depends(get_db)):
    mascotas = (
        db.query(
            Mascota,
            Especie.nombre_especie,
            Raza.nombre_raza,
            Raza.id_especie
        )
        .join(Raza, Mascota.id_raza == Raza.id_raza)
        .join(Especie, Raza.id_especie == Especie.id_especie)
        .filter(Mascota.id_usuario == usuario_id)
        .all()
    )

    mascotas = [
        MascotaSchema(
            id_mascota=m.id_mascota,
            nombre_mascota=m.nombre_mascota,
            id_raza=m.id_raza,
            sexo=m.sexo,
            fecha_nacimiento=m.fecha_nacimiento,
            id_usuario=m.id_usuario,
            fecha_registro=m.fecha_registro,
            id_especie=id_especie,
            nombre_raza=nombre_raza,
            nombre_especie=nombre_especie
        )
        for m, nombre_especie, nombre_raza, id_especie in mascotas_db
    ]


    return mascotas