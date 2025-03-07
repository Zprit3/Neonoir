from app import create_app
from extensions import db
from models import Personaje

def init_personajes():
    """Inicializa la tabla Personajes con datos predefinidos."""

    app = create_app()
    with app.app_context():
        personajes = [
            Personaje(nombre="Guerrero Valiente", vida=120, estadisticaPrincipal=15),
            Personaje(nombre="Mago Astuto", vida=80, estadisticaPrincipal=20),
            Personaje(nombre="Pícaro Ágil", vida=100, estadisticaPrincipal=18),
            Personaje(nombre="Clérigo Sabio", vida=110, estadisticaPrincipal=16),
            # Agrega más personajes según sea necesario
        ]

        for personaje in personajes:
            db.session.add(personaje)

        db.session.commit()
        print("Tabla Personajes inicializada.")

if __name__ == "__main__":
    init_personajes()