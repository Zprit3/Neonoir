from app import create_app
from extensions import db
from models import Zona

def init_zonas():
    """Inicializa la tabla Zonas con datos predefinidos."""

    app = create_app()
    with app.app_context():
        zonas = [
            Zona(tipoZona="neutra", nombre="Claro Tranquilo", descripcion="Un claro tranquilo en el bosque. No hay peligros inmediatos, pero tampoco beneficios."),
            Zona(tipoZona="positiva", nombre="Manantial Curativo", recuperacionVida=15, descripcion="Un manantial de aguas cristalinas. Te sientes revitalizado y tus heridas sanan."),
            Zona(tipoZona="negativa", nombre="Ciénaga Oscura", modificacionVida=-10, descripcion="Una ciénaga oscura y pantanosa. El aire está cargado de miasmas y sientes que tu energía vital se drena."),
            Zona(tipoZona="descanso", nombre="Posada Acogedora", descripcion="Una posada acogedora con chimenea y camas cómodas. Un lugar perfecto para descansar y recuperarte."),
            Zona(tipoZona="victoria", nombre="Castillo del Rey Oscuro", descripcion="El castillo del Rey Oscuro. La batalla final te espera."),
        ]

        for zona in zonas:
            db.session.add(zona)

        db.session.commit()
        print("Tabla Zonas inicializada.")

if __name__ == "__main__":
    init_zonas()