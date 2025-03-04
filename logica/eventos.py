from extensions import db
from models import PersonajePartida

def aplicar_efecto_evento(personaje, evento, partida_id):
    personaje_partida = PersonajePartida.query.filter_by(partidaId=partida_id, personajeId=personaje.id).first()
    personaje_partida.vida += evento.modificacionVida
    personaje_partida.posicion += evento.avanceCasillas
    db.session.commit()