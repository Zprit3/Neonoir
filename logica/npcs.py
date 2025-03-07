from app import socketio

def interactuar_npc(personaje, npc):
    print(npc.dialogo)
    socketio.emit('dialogo_npc', {'npc_id': npc.id, 'dialogo': npc.dialogo}, room=f'personaje_{personaje.id}') #emitir dialogo del npc.