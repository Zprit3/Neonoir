from models import ObjetoVictoria, PersonajePartida
from app import socketio

def verificar_condiciones_victoria(partida_id, personaje_id):
    objeto_victoria = ObjetoVictoria.query.first()
    personaje_partida = PersonajePartida.query.filter_by(partidaId=partida_id, personajeId=personaje_id).first()
    if objeto_victoria and personaje_partida.objetos_victoria >= objeto_victoria.cantidad_necesaria:
        print("¡Has ganado la partida!")
        socketio.emit('partida_ganada', {'personaje_id': personaje_id}, room=partida_id) #emitir partida ganada.
        # Lógica para finalizar la partida