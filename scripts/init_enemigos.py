from app import create_app
from extensions import db
from models import Enemigo

def init_enemigos():

    app = create_app()
    with app.app_context():
        enemigos = [
            Enemigo(nombre="Goblin", vida=10, tipo="debil", oroDrop=5, descripcion="Un pequeño y astuto goblin. No representa una gran amenaza, pero puede sorprenderte con su agilidad."),
            Enemigo(nombre="Orco", vida=25, tipo="normal", oroDrop=10, descripcion="Un guerrero orco fornido y brutal. Su fuerza bruta es su principal arma."),
            Enemigo(nombre="Troll", vida=40, tipo="fuerte", oroDrop=15, descripcion="Un troll enorme y regenerativo. Su piel gruesa lo protege de los ataques y su fuerza es devastadora."),
            Enemigo(nombre="Espectro", vida=15, tipo="normal", oroDrop=8, descripcion="Un ser incorpóreo que se alimenta de la energía vital. Sus ataques pueden debilitarte rápidamente."),
            Enemigo(nombre="Dragón", vida=60, tipo="fuerte", oroDrop=20, descripcion="Una criatura legendaria con aliento de fuego y escamas impenetrables. Un enemigo formidable."),
            
        ]

        for enemigo in enemigos:
            db.session.add(enemigo)

        db.session.commit()
        print("Tabla Enemigos inicializada.")

if __name__ == "__main__":
    init_enemigos()