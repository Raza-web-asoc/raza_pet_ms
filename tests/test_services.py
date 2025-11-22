import pytest
from pydantic import ValidationError

from app.schemas.mascota import MascotaCreate
from app.schemas.raza import RazaCreate


def test_mascota_schema_requires_fields():
    # nombre_mascota es obligatorio
    with pytest.raises(ValidationError):
        MascotaCreate(id_raza=1, sexo='M', fecha_nacimiento='2020-01-01')


def test_raza_schema_accepts_valid_data():
    r = RazaCreate(nombre_raza='Labrador', id_especie=1)
    assert r.nombre_raza == 'Labrador'
    assert r.id_especie == 1
