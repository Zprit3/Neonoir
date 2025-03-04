from models import Partida, PersonajePartida

def verificar_condiciones_victoria(partida_id, personaje_id):
    partida = Partida.query.get(partida_id)
    personaje_partida = PersonajePartida.query.filter_by(partidaId=partida_id, personajeId=personaje_id).first()

    # Lógica para verificar las condiciones de victoria
    if personaje_partida.objetoVictoria:
        print("¡El jugador ha ganado!")
    else:
        print("El jugador aún no ha ganado.")