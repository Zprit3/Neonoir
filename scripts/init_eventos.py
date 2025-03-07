from app import create_app
from extensions import db
from models import Evento

def init_eventos():
    """Inicializa la tabla Eventos con datos predefinidos."""

    app = create_app()
    with app.app_context():
        eventos = [
            Evento(nombre="Encuentro con un Viajero", descripcion="Te encuentras con un viajero cansado que te ofrece información valiosa a cambio de algo de comida.", modificacionOro=10, modificacionVida=-5),
            Evento(nombre="Trampa en el Camino", descripcion="Caes en una trampa oculta y sufres algunas heridas.", modificacionVida=-15),
            Evento(nombre="Hallazgo de un Tesoro", descripcion="Encuentras un cofre oculto con valiosas monedas de oro.", modificacionOro=30),
            Evento(nombre="Tormenta repentina", descripcion="Una tormenta repentina te obliga a buscar refugio. Pierdes tiempo y recursos.", avanceCasillas=-1, modificacionOro=-5),
            Evento(nombre="Bendición de los Dioses", descripcion="Sientes una energía divina que te revitaliza y te cura.", modificacionVida=20),
            # Agrega más eventos según sea necesario
        ]

        for evento in eventos:
            db.session.add(evento)

        db.session.commit()
        print("Tabla Eventos inicializada.")

if __name__ == "__main__":
    init_eventos()