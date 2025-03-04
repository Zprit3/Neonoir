from extensions import db
from models import PersonajePartida, Enemigo
import random

def iniciar_combate(partida_id, personaje_id, enemigo_id):
    personaje = PersonajePartida.query.filter_by(partidaId=partida_id, personajeId=personaje_id).first()
    enemigo = Enemigo.query.get(enemigo_id)

    ataque_personaje = random.randint(1, 20) + 10 #10 es la estadistica principal
    ataque_enemigo = random.randint(1, 20)

    if ataque_personaje > ataque_enemigo:
        dmg = (ataque_personaje - ataque_enemigo) + 5
        enemigo.vida -= dmg
    elif ataque_enemigo > ataque_personaje:
        dmg = (ataque_enemigo - ataque_personaje) + 3
        personaje.vida -= dmg

    db.session.commit()