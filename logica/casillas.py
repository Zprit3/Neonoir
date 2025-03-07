from extensions import db
from models import CasillaContenido, Enemigo, Evento, Zona, Npc, PersonajePartida
from logica.combate import iniciar_combate
from logica.eventos import aplicar_efecto_evento
from logica.zonas import aplicar_efecto_zona
from logica.npcs import interactuar_npc
from logica.condiciones_victoria import verificar_condiciones_victoria #importamos
from app import socketio 

def aplicar_efectos_casilla(personaje, casilla, partida_id):
    contenidos = CasillaContenido.query.filter_by(casillaId=casilla.id).all()
    for contenido in contenidos:
        if contenido.contenidoTipo == 'enemigo':
            enemigo = Enemigo.query.get(contenido.contenidoId)
            iniciar_combate(partida_id, personaje.id, enemigo.id)
            socketio.emit('combate_iniciado', {'personaje_id': personaje.id, 'enemigo_id': enemigo.id}, room=partida_id) #emitir inicio de combate.
        elif contenido.contenidoTipo == 'evento':
            evento = Evento.query.get(contenido.contenidoId)
            aplicar_efecto_evento(personaje, evento, partida_id)
            socketio.emit('evento_aplicado', {'personaje_id': personaje.id, 'evento_id': evento.id}, room=partida_id) #emitir aplicacion de evento.
        elif contenido.contenidoTipo == 'zona':
            zona = Zona.query.get(contenido.contenidoId)
            aplicar_efecto_zona(personaje, zona, partida_id)
            socketio.emit('zona_aplicada', {'personaje_id': personaje.id, 'zona_id': zona.id}, room=partida_id) #emitir aplicacion de zona.
        elif contenido.contenidoTipo == 'npc':
            npc = Npc.query.get(contenido.contenidoId)
            interactuar_npc(personaje, npc)
            socketio.emit('npc_interaccion', {'personaje_id': personaje.id, 'npc_id': npc.id}, room=partida_id) #emitir interaccion con npc.
    verificar_condiciones_victoria(partida_id, personaje.id)
    socketio.emit('condiciones_victoria_verificadas', {'personaje_id': personaje.id}, room=partida_id) #emitir verificacion de condiciones de victoria.