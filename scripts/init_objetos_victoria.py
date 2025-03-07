from app import create_app
from extensions import db
from models import ObjetoVictoria

def init_objetos_victoria():
    """Inicializa la tabla ObjetosVictoria con datos predefinidos."""

    app = create_app()
    with app.app_context():
        objetos_victoria = [
            ObjetoVictoria(nombre="Amuleto del Dragón", descripcion="Un amuleto mágico que contiene el poder de un dragón ancestral."),
            ObjetoVictoria(nombre="Cetro del Rey Oscuro", descripcion="El cetro que otorga el poder para gobernar las tierras oscuras."),
            ObjetoVictoria(nombre="Gema de la Luz Eterna", descripcion="Una gema que emana una luz sagrada capaz de disipar la oscuridad."),
            ObjetoVictoria(nombre="Reliquia de los Dioses Antiguos", descripcion="Una reliquia que contiene el poder de los dioses antiguos y otorga la inmortalidad."),
            ObjetoVictoria(nombre="Mapa del Tesoro Perdido", descripcion="Un mapa que conduce a un tesoro legendario custodiado por criaturas peligrosas."),
            # Agrega más objetos de victoria según sea necesario
        ]

        for objeto in objetos_victoria:
            db.session.add(objeto)

        db.session.commit()
        print("Tabla ObjetosVictoria inicializada.")

if __name__ == "__main__":
    init_objetos_victoria()