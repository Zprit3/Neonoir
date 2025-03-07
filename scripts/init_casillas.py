from app import create_app
from extensions import db
from models import Casilla

def init_casillas():

    app = create_app()
    with app.app_context():
        casillas = [
            Casilla(tipo="inicio"),
            Casilla(tipo="camino_bosque"),
            Casilla(tipo="claro_lago"),
            Casilla(tipo="montaña_rocosa"),
            Casilla(tipo="cueva_oscura"),
            Casilla(tipo="pueblo_mercaderes"),
            Casilla(tipo="templo_antiguo"),
            Casilla(tipo="castillo_rey_oscuro"),
            Casilla(tipo="descanso"),
           
        ]

        for casilla in casillas:
            db.session.add(casilla)

        db.session.commit()
        print("Tabla Casillas inicializada.")

if __name__ == "__main__":
    init_casillas()