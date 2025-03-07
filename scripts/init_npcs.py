from app import create_app
from extensions import db
from models import Npc

def init_npcs():
    """Inicializa la tabla NPCs con datos predefinidos."""

    app = create_app()
    with app.app_context():
        npcs = [
            Npc(nombre="Anciano Sabio", dialogo="Saludos, joven aventurero. El camino que tienes por delante es peligroso, pero si sigues tu corazón, encontrarás la victoria."),
            Npc(nombre="Comerciante Errante", dialogo="¡Bienvenido a mi humilde tienda! Tengo mercancías raras y valiosas que podrían interesarte."),
            Npc(nombre="Guardián del Bosque", dialogo="No puedes pasar por aquí. El bosque está protegido por fuerzas antiguas y solo aquellos dignos pueden entrar."),
            Npc(nombre="Mago Misterioso", dialogo="Las estrellas me han revelado tu destino. Pero recuerda, el futuro no está escrito en piedra."),
            Npc(nombre="Caballero Herido", dialogo="Necesito ayuda... Fui atacado por criaturas oscuras y mis heridas son graves."),
            # Agrega más NPCs según sea necesario
        ]

        for npc in npcs:
            db.session.add(npc)

        db.session.commit()
        print("Tabla NPCs inicializada.")

if __name__ == "__main__":
    init_npcs()