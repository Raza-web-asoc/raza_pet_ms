from sqlalchemy import Column, Integer, String, Text, Enum, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Especie(Base):
    __tablename__ = 'especie'
    id_especie = Column(Integer, primary_key=True, autoincrement=True)
    nombre_especie = Column(String(100), nullable=False, unique=True, comment='Nombre de la especie (e.g., perro, gato, ave)')

    razas = relationship("Raza", back_populates="especie")

class Raza(Base):
    __tablename__ = 'raza'
    id_raza = Column(Integer, primary_key=True, autoincrement=True)
    nombre_raza = Column(String(100), nullable=False, comment='Nombre de la raza de la mascota')
    id_especie = Column(Integer, ForeignKey('especie.id_especie', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, comment='Relación con la especie')

    especie = relationship('Especie', back_populates='razas')


class Mascota(Base):
    __tablename__ = 'mascotas'
    id_mascota = Column(Integer, primary_key=True, autoincrement=True)
    nombre_mascota = Column(String(100), nullable=False, comment='Nombre de la mascota')
    id_raza = Column(Integer, ForeignKey('raza.id_raza', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, comment='Relación con la raza')
    sexo = Column(Enum('M', 'F'), nullable=False, comment='Género de la mascota')
    fecha_nacimiento = Column(Date, nullable=False, comment='Fecha de nacimiento de la mascota')
    id_usuario = Column(Integer, nullable=False, comment='Usuario dueño de la mascota')
    fecha_registro = Column(DateTime, default=datetime.utcnow, comment='Fecha de registro de la mascota')

    raza = relationship('Raza')
