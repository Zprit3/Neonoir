from app import socketio
from flask_socketio import emit, join_room, leave_room
from models import PersonajePartida, PersonajeTarjetas, db, Tarjeta

def configure_sockets(socketio): #se agrega la funcion configure sockets, para configurar los sockets desde app.py
    @socketio.on('connect')
    def handle_connect():
        print('Cliente conectado')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Cliente desconectado')

    @socketio.on('join_partida')
    def handle_join_partida(data):
        partida_id = data['partida_id']
        join_room(partida_id)
        print(f'Cliente unido a la partida {partida_id}')
        emit('mensaje', {'mensaje': f'Te has unido a la partida {partida_id}'}, room=partida_id)

    @socketio.on('leave_partida')
    def handle_leave_partida(data):
        partida_id = data['partida_id']
        leave_room(partida_id)
        print(f'Cliente abandonó la partida {partida_id}')
        emit('mensaje', {'mensaje': f'Has abandonado la partida {partida_id}'}, room=partida_id)

    @socketio.on('mover_personaje')
    def handle_mover_personaje(data):
        partida_id = data['partida_id']
        personaje_id = data['personaje_id']
        nueva_posicion = data['nueva_posicion']

        personaje_partida = PersonajePartida.query.filter_by(partida_id=partida_id, personaje_id=personaje_id).first()
        if personaje_partida:
            personaje_partida.posicion = nueva_posicion
            db.session.commit()
            emit('personaje_movido', {'personaje_id': personaje_id, 'nueva_posicion': nueva_posicion}, room=partida_id)
        else:
            emit('error', {'mensaje': 'Personaje no encontrado en la partida'}, room=partida_id)

@socketio.on('usar_tarjeta')
def handle_usar_tarjeta(data):
    partida_id = data['partida_id']
    personaje_id = data['personaje_id']
    tarjeta_id = data['tarjeta_id']
    objetivo_id = data.get('objetivo_id')

    personaje_partida = PersonajePartida.query.filter_by(partida_id=partida_id, personaje_id=personaje_id).first()
    tarjeta = Tarjeta.query.get(tarjeta_id)

    if not personaje_partida or not tarjeta:
        emit('error', {'mensaje': 'Personaje o tarjeta no encontrados'}, room=partida_id)
        return

    # Validar la tarjeta (ejemplo: verificar si el personaje tiene la tarjeta en su inventario)
    tarjeta_en_inventario = PersonajeTarjetas.query.filter_by(personaje_id=personaje_id, tarjeta_id=tarjeta_id).first()
    if not tarjeta_en_inventario:
        emit('error', {'mensaje': 'El personaje no posee esta tarjeta'}, room=partida_id)
        return

    # Aplicar el efecto según el tipo de tarjeta y su valor
    if tarjeta.efecto == 'daño_directo' and objetivo_id:
        objetivo = PersonajePartida.query.filter_by(partida_id=partida_id, personaje_id=objetivo_id).first()
        if objetivo:
            objetivo.vida -= tarjeta.valor
            db.session.commit()
            emit('mensaje', {'mensaje': f'{personaje_partida.personaje.nombre} inflige {tarjeta.valor} de daño a {objetivo.personaje.nombre}'}, room=partida_id)
        else:
            emit('error', {'mensaje': 'Objetivo no encontrado'}, room=partida_id)
    elif tarjeta.efecto == 'curacion':
        personaje_partida.vida += tarjeta.valor
        db.session.commit()
        emit('mensaje', {'mensaje': f'{personaje_partida.personaje.nombre} se cura {tarjeta.valor} puntos de vida'}, room=partida_id)
    # ... otros efectos

    # Lógica para descartar la tarjeta
    if tarjeta.unica:
        # Eliminar la tarjeta del inventario del personaje
        PersonajeTarjetas.query.filter_by(personaje_id=personaje_id, tarjeta_id=tarjeta_id).delete()
        db.session.commit()
        emit('mensaje', {'mensaje': f'{personaje_partida.personaje.nombre} descarta la tarjeta {tarjeta.nombre} (única)'}, room=partida_id)
    elif tarjeta.duracion == 0:
        # Descartar la tarjeta inmediatamente
        PersonajeTarjetas.query.filter_by(personaje_id=personaje_id, tarjeta_id=tarjeta_id).delete()
        db.session.commit()
        emit('mensaje', {'mensaje': f'{personaje_partida.personaje.nombre} descarta la tarjeta {tarjeta.nombre}'}, room=partida_id)
    else:
        # La tarjeta dura varios turnos, reducir la duración
        tarjeta_en_inventario.cantidad -= 1
        if tarjeta_en_inventario.cantidad == 0:
            PersonajeTarjetas.query.filter_by(personaje_id=personaje_id, tarjeta_id=tarjeta_id).delete()
            db.session.commit()
            emit('mensaje', {'mensaje': f'{personaje_partida.personaje.nombre} descarta la tarjeta {tarjeta.nombre}'}, room=partida_id)
        else:
            db.session.commit()

    emit('tarjeta_usada', {'personaje_id': personaje_id, 'tarjeta_id': tarjeta_id, 'objetivo_id': objetivo_id}, room=partida_id)