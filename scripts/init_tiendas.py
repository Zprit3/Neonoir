from app import create_app
from extensions import db
from models import Tienda

def init_tiendas():
    """Inicializa la tabla Tiendas con datos predefinidos."""

    app = create_app()
    with app.app_context():
        tiendas = [
            Tienda(nombre="Tienda de Armas y Armaduras", tarjetas_venta=[{"tarjeta_id": 1, "precio": 20}, {"tarjeta_id": 2, "precio": 30}]),
            Tienda(nombre="Tienda de Pociones y Curaciones", tarjetas_venta=[{"tarjeta_id": 3, "precio": 15}, {"tarjeta_id": 4, "precio": 25}]),
            Tienda(nombre="Tienda de Objetos Mágicos", tarjetas_venta=[{"tarjeta_id": 5, "precio": 40}, {"tarjeta_id": 6, "precio": 50}]),
            Tienda(nombre="Tienda de Tarjetas de Apoyo", tarjetas_venta=[{"tarjeta_id": 7, "precio": 10}, {"tarjeta_id": 8, "precio": 18}]),
            Tienda(nombre="Tienda de Tarjetas de Ataque", tarjetas_venta=[{"tarjeta_id": 9, "precio": 22}, {"tarjeta_id": 10, "precio": 35}]),
            # Agrega más tiendas según sea necesario
        ]

        for tienda in tiendas:
            db.session.add(tienda)

        db.session.commit()
        print("Tabla Tiendas inicializada.")

if __name__ == "__main__":
    init_tiendas()