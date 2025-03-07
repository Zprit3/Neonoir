from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import PersonajePartida
from app import socketio

personajes_partidas_bp = Blueprint('personajes_partidas', __name__)

MENSAJE = 'Estado de personaje en partida no encontrado'
INV_CSRF = 'CSRF token inválido'

@personajes_partidas_bp.route('/', methods=['GET'])
@csrf.exempt
def obtener_personajes_partidas():
    personajes_partidas = PersonajePartida.query.all()
    lista_personajes_partidas = [{'id': personaje_partida.id, 'partidaId': personaje_partida.partidaId, 'personajeId': personaje_partida.personajeId, 'posicion': personaje_partida.posicion, 'vida': personaje_partida.vida} for personaje_partida in personajes_partidas]
    return jsonify(lista_personajes_partidas)

@personajes_partidas_bp.route('/<int:personaje_partida_id>', methods=['GET'])
@csrf.exempt
def obtener_personaje_partida(personaje_partida_id):
    personaje_partida = PersonajePartida.query.get(personaje_partida_id)
    if not personaje_partida:
        return jsonify({'mensaje': MENSAJE}), 404
    return jsonify({'id': personaje_partida.id, 'partidaId': personaje_partida.partidaId, 'personajeId': personaje_partida.personajeId, 'posicion': personaje_partida.posicion, 'vida': personaje_partida.vida})

@personajes_partidas_bp.route('/', methods=['POST'])
def crear_personaje_partida():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': INV_CSRF}), 400
    data = request.get_json()
    partida_id = data.get('partidaId')
    personaje_id = data.get('personajeId')
    if not partida_id or not personaje_id:
        return jsonify({'mensaje': 'partidaId y personajeId son requeridos'}), 400
    nuevo_personaje_partida = PersonajePartida(partidaId=partida_id, personajeId=personaje_id)
    db.session.add(nuevo_personaje_partida)
    db.session.commit()
    return jsonify({'mensaje': 'Estado de personaje en partida creado', 'id': nuevo_personaje_partida.id}), 201

@personajes_partidas_bp.route('/<int:personaje_partida_id>', methods=['PUT'])
def actualizar_personaje_partida(personaje_partida_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': INV_CSRF}), 400
    personaje_partida = PersonajePartida.query.get(personaje_partida_id)
    if not personaje_partida:
        return jsonify({'mensaje': MENSAJE}), 404
    data = request.get_json()
    partida_id = personaje_partida.partidaId #obtener el id de la partida antes de la actualizacion.
    personaje_partida.partidaId = data.get('partidaId', personaje_partida.partidaId)
    personaje_partida.personajeId = data.get('personajeId', personaje_partida.personajeId)
    personaje_partida.posicion = data.get('posicion', personaje_partida.posicion)
    personaje_partida.vida = data.get('vida', personaje_partida.vida)
    db.session.commit()
    socketio.emit('personaje_partida_actualizado', {'personaje_partida_id': personaje_partida_id, 'posicion': personaje_partida.posicion, 'vida': personaje_partida.vida}, room=partida_id) #emitir actualizacion
    return jsonify({'mensaje': 'Estado de personaje en partida actualizado'})

@personajes_partidas_bp.route('/<int:personaje_partida_id>', methods=['DELETE'])
def eliminar_personaje_partida(personaje_partida_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': INV_CSRF}), 400
    personaje_partida = PersonajePartida.query.get(personaje_partida_id)
    if not personaje_partida:
        return jsonify({'mensaje': MENSAJE}), 404
    db.session.delete(personaje_partida)
    db.session.commit()
    return jsonify({'mensaje': 'Estado de personaje en partida eliminado'})