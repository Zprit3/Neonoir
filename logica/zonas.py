from extensions import db
from models import PersonajePartida

def aplicar_efecto_zona(personaje, zona, partida_id):
    personaje_partida = PersonajePartida.query.filter_by(partidaId=partida_id, personajeId=personaje.id).first()
    personaje_partida.vida += zona.modificacionVida
    db.session.commit()