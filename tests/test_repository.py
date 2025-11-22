import pytest
from unittest import mock
from fastapi import HTTPException

from app.controllers import mascota as mascota_controller
from app.schemas.mascota import MascotaCreate, MascotaUpdate


def test_read_mascota_not_found():
    mock_db = mock.Mock()
    # Encadenado de llamadas: query().join().join().filter().first() -> None
    mock_db.query.return_value.join.return_value.join.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        mascota_controller.read_mascota(1, db=mock_db)
    assert exc.value.status_code == 404


def test_read_mascota_success():
    class Dummy:
        def __init__(self):
            self.id_mascota = 1
            self.nombre_mascota = 'Fido'
            self.id_raza = 1
            self.sexo = 'M'
            self.fecha_nacimiento = '2020-01-01'
            self.id_usuario = 1
            self.fecha_registro = None

    dummy = Dummy()
    mock_db = mock.Mock()
    mock_db.query.return_value.join.return_value.join.return_value.filter.return_value.first.return_value = (dummy, 'Perro', 'Labrador', 1)

    result = mascota_controller.read_mascota(1, db=mock_db)
    assert result['id_mascota'] == 1
    assert result['nombre_raza'] == 'Labrador'
    assert result['nombre_especie'] == 'Perro'


def test_create_mascota_requires_header_and_calls_db():
    # Preparar un mock para la DB
    mock_db = mock.Mock()
    mascota_in = MascotaCreate(nombre_mascota='Rex', id_raza=1, sexo='M', fecha_nacimiento='2020-01-01')

    # Sin header debe lanzar excepción
    with pytest.raises(HTTPException) as exc:
        mascota_controller.create_mascota(mascota_in, x_auth_user_id=None, db=mock_db)
    assert exc.value.status_code == 400

    # Con header debe llamar a add/commit/refresh
    mascota_controller.create_mascota(mascota_in, x_auth_user_id='2', db=mock_db)
    assert mock_db.add.called
    assert mock_db.commit.called
    assert mock_db.refresh.called
