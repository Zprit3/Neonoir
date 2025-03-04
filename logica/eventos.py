from extensions import db
from models import PersonajePartida

def aplicar_efecto_evento(personaje, evento, partida_id):
    personaje_partida = PersonajePartida.query.filter_by(partidaId=partida_id, personajeId=personaje.id).first()

    # Modificación de vida
    personaje_partida.vida += evento.modificacionVida

    # Modificación de oro
    personaje_partida.oro += evento.modificacionOro

    # Avance/retroceso de casillas
    personaje_partida.posicion += evento.avanceCasillas

    # Debuffs
    if evento.debuffEstadistica:
        # Lógica para aplicar el debuff (por ejemplo, agregar a un diccionario de debuffs en PersonajePartida)
        pass

    db.session.commit()