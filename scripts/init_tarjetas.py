from app import create_app
from extensions import db
from models import Tarjeta

def init_tarjetas():
    """Inicializa la tabla Tarjetas con datos predefinidos."""

    app = create_app()
    with app.app_context():
        tarjetas = [
            Tarjeta(nombre="Espada Afilada", descripcion="Aumenta el ataque en 5 puntos.", tipo="ataque", efecto="aumentar_ataque", duracion=1),
            Tarjeta(nombre="Armadura Reforzada", descripcion="Aumenta la defensa en 3 puntos.", tipo="defensa", efecto="aumentar_defensa", duracion=2),
            Tarjeta(nombre="Poción Curativa", descripcion="Restaura 20 puntos de vida.", tipo="curacion", efecto="restaurar_vida", duracion=0),
            Tarjeta(nombre="Bendición Divina", descripcion="Elimina todos los debuffs.", tipo="apoyo", efecto="eliminar_debuffs", duracion=0),
            Tarjeta(nombre="Bola de Fuego", descripcion="Inflige 30 puntos de daño mágico.", tipo="ataque", efecto="daño_magico", duracion=1),
            Tarjeta(nombre="Escudo Mágico", descripcion="Reduce el daño recibido en 15 puntos.", tipo="defensa", efecto="reducir_daño", duracion=2),
            Tarjeta(nombre="Elixir de Velocidad", descripcion="Aumenta la velocidad en 2 puntos.", tipo="apoyo", efecto="aumentar_velocidad", duracion=3),
            Tarjeta(nombre="Maldición Oscura", descripcion="Reduce la vida del enemigo en 25 puntos.", tipo="ataque", efecto="reducir_vida_enemigo", duracion=1),
            Tarjeta(nombre="Armadura de Espinas", descripcion="Refleja el 50% del daño recibido.", tipo="defensa", efecto="reflejar_daño", duracion=2),
            Tarjeta(nombre="Poción de Invisibilidad", descripcion="Te hace invisible para los enemigos durante 2 turnos.", tipo="apoyo", efecto="invisibilidad", duracion=2),
            # Agrega más tarjetas según sea necesario
        ]

        for tarjeta in tarjetas:
            db.session.add(tarjeta)

        db.session.commit()
        print("Tabla Tarjetas inicializada.")

if __name__ == "__main__":
    init_tarjetas()