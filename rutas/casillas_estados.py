from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import CasillaEstado
from app import socketio

casillas_estados_bp = Blueprint('casillas_estados', __name__)

CASILLA_EST_NF = 'Estado de casilla no encontrado'
CSRF_INV = 'CSRF token inválido'

@casillas_estados_bp.route('/', methods=['GET'])
@csrf.exempt
def obtener_casillas_estados():
    casillas_estados = CasillaEstado.query.all()
    lista_casillas_estados = [{'id': casilla_estado.id, 'partidaId': casilla_estado.partidaId, 'casillaId': casilla_estado.casillaId, 'contenidoId': casilla_estado.contenidoId, 'contenidoTipo': casilla_estado.contenidoTipo} for casilla_estado in casillas_estados]
    return jsonify(lista_casillas_estados)

@casillas_estados_bp.route('/<int:casilla_estado_id>', methods=['GET'])
@csrf.exempt
def obtener_casilla_estado(casilla_estado_id):
    casilla_estado = CasillaEstado.query.get(casilla_estado_id)
    if not casilla_estado:
        return jsonify({'mensaje': CASILLA_EST_NF}), 404
    return jsonify({'id': casilla_estado.id, 'partidaId': casilla_estado.partidaId, 'casillaId': casilla_estado.casillaId, 'contenidoId': casilla_estado.contenidoId, 'contenidoTipo': casilla_estado.contenidoTipo})

@casillas_estados_bp.route('/', methods=['POST'])
def crear_casilla_estado():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    data = request.get_json()
    partida_id = data.get('partidaId')
    casilla_id = data.get('casillaId')
    contenido_id = data.get('contenidoId')
    contenido_tipo = data.get('contenidoTipo')
    if not partida_id or not casilla_id:
        return jsonify({'mensaje': 'partidaId y casillaId son requeridos'}), 400
    nuevo_casilla_estado = CasillaEstado(partidaId=partida_id, casillaId=casilla_id, contenidoId=contenido_id, contenidoTipo=contenido_tipo)
    db.session.add(nuevo_casilla_estado)
    db.session.commit()
    socketio.emit('casilla_estado_creado',{'partida_id':partida_id, 'casilla_id':casilla_id, 'contenido_id': contenido_id, 'contenido_tipo': contenido_tipo}, room=partida_id) #emitir creacion.
    return jsonify({'mensaje': 'Estado de casilla creado', 'id': nuevo_casilla_estado.id}), 201

@casillas_estados_bp.route('/<int:casilla_estado_id>', methods=['PUT'])
def actualizar_casilla_estado(casilla_estado_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    casilla_estado = CasillaEstado.query.get(casilla_estado_id)
    if not casilla_estado:
        return jsonify({'mensaje': CASILLA_EST_NF}), 404
    data = request.get_json()
    partida_id = casilla_estado.partidaId #obtener el id de la partida antes de la actualizacion.
    casilla_estado.partidaId = data.get('partidaId', casilla_estado.partidaId)
    casilla_estado.casillaId = data.get('casillaId', casilla_estado.casillaId)
    casilla_estado.contenidoId = data.get('contenidoId', casilla_estado.contenidoId)
    casilla_estado.contenidoTipo = data.get('contenidoTipo', casilla_estado.contenidoTipo)
    db.session.commit()
    socketio.emit('casilla_estado_actualizado', {'casilla_estado_id': casilla_estado_id, 'contenido_id': casilla_estado.contenidoId, 'contenido_tipo': casilla_estado.contenidoTipo}, room=partida_id) #emitir actualizacion
    return jsonify({'mensaje': 'Estado de casilla actualizado'})

@casillas_estados_bp.route('/<int:casilla_estado_id>', methods=['DELETE'])
def eliminar_casilla_estado(casilla_estado_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    casilla_estado = CasillaEstado.query.get(casilla_estado_id)
    if not casilla_estado:
        return jsonify({'mensaje': CSRF_INV}), 404
    partida_id = casilla_estado.partidaId #obtener el id de la partida antes de la eliminacion.
    db.session.delete(casilla_estado)
    db.session.commit()
    socketio.emit('casilla_estado_eliminado', {'casilla_estado_id': casilla_estado_id}, room=partida_id) #emitir eliminacion
    return jsonify({'mensaje': 'Estado de casilla eliminado'})