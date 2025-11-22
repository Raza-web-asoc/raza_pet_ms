import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base_class import Base
from app.db.session import get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_create_and_get_flow():
    # Crear especie
    resp = client.post("/especies/", json={"nombre_especie": "Perro"})
    assert resp.status_code == 200
    especie = resp.json()
    assert "id_especie" in especie

    # Crear raza
    resp = client.post("/razas/", json={"nombre_raza": "Labrador", "id_especie": especie["id_especie"]})
    assert resp.status_code == 200
    raza = resp.json()
    assert "id_raza" in raza

    # Crear mascota
    mascota_payload = {
        "nombre_mascota": "Fido",
        "id_raza": raza["id_raza"],
        "sexo": "M",
        "fecha_nacimiento": "2020-01-01"
    }
    headers = {"x-auth-user-id": "1"}
    resp = client.post("/mascotas/", json=mascota_payload, headers=headers)
    assert resp.status_code == 200
    mascota = resp.json()
    assert "id_mascota" in mascota

    # Listar mascotas
    resp = client.get("/mascotas/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(m["id_mascota"] == mascota["id_mascota"] for m in data)

    # Obtener mascota por id
    resp = client.get(f"/mascotas/{mascota['id_mascota']}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id_mascota"] == mascota["id_mascota"]

