from app import create_app
from extensions import db
from models import Jugador

def init_jugadores():
    """Inicializa la tabla Jugadores con datos de prueba."""

    app = create_app()
    with app.app_context():
        jugadores = [
            Jugador(nombreUsuario="testuser1", contrasena="testpass1"),
            Jugador(nombreUsuario="testuser2", contrasena="testpass2"),
        ]

        for jugador in jugadores:
            jugador.set_password(jugador.contrasena) # Encripta la contraseña
            db.session.add(jugador)

        db.session.commit()
        print("Tabla Jugadores inicializada con usuarios de prueba.")

if __name__ == "__main__":
    init_jugadores()