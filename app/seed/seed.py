from app.db.session import get_db
from app.db.models import Especie, Raza

def run_seed():
    db = next(get_db())   # ← aquí está el cambio importante

    # 2. Crear especie “Perro”
    especie_perro = db.query(Especie).filter_by(nombre_especie="Perro").first()

    if not especie_perro:
        especie_perro = Especie(nombre_especie="Perro")
        db.add(especie_perro)
        db.commit()
        db.refresh(especie_perro)
        print("✔ Especie 'Perro' creada")

    # 3. Crear razas
    razas = ["Labrador", "Pug", "Golden Retriever", "Pastor Alemán"]

    for r in razas:
        if not db.query(Raza).filter_by(nombre_raza=r).first():
            raza = Raza(nombre_raza=r, id_especie=especie_perro.id_especie)
            db.add(raza)
            print(f"✔ Raza '{r}' creada")

    db.commit()
