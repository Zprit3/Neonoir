from extensions import db
from models import PersonajePartida, Npc
from app import socketio 

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
        personaje_partida.debuffs[evento.debuffEstadistica] = 3 #3 es la cantidad de turnos que dura el debuff

    # Aparición de NPC
    if evento.npcId:
        npc = Npc.query.get(evento.npcId)
        if npc:
            print(npc.dialogo) #muestra el dialogo del npc
            socketio.emit('npc_aparece', {'npc_id': npc.id}, room=partida_id) #emitir aparicion de npc.
            #puedes agregar aqui logica para que el npc se quede en la casilla o se mueva

    db.session.commit()