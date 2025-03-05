from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import CasillaEstado

casillas_estados_bp = Blueprint('casillas_estados', __name__)

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
        return jsonify({'mensaje': 'Estado de casilla no encontrado'}), 404
    return jsonify({'id': casilla_estado.id, 'partidaId': casilla_estado.partidaId, 'casillaId': casilla_estado.casillaId, 'contenidoId': casilla_estado.contenidoId, 'contenidoTipo': casilla_estado.contenidoTipo})

@casillas_estados_bp.route('/', methods=['POST'])
def crear_casilla_estado():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
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
    return jsonify({'mensaje': 'Estado de casilla creado', 'id': nuevo_casilla_estado.id}), 201

@casillas_estados_bp.route('/<int:casilla_estado_id>', methods=['PUT'])
def actualizar_casilla_estado(casilla_estado_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
    casilla_estado = CasillaEstado.query.get(casilla_estado_id)
    if not casilla_estado:
        return jsonify({'mensaje': 'Estado de casilla no encontrado'}), 404
    data = request.get_json()
    casilla_estado.partidaId = data.get('partidaId', casilla_estado.partidaId)
    casilla_estado.casillaId = data.get('casillaId', casilla_estado.casillaId)
    casilla_estado.contenidoId = data.get('contenidoId', casilla_estado.contenidoId)
    casilla_estado.contenidoTipo = data.get('contenidoTipo', casilla_estado.contenidoTipo)
    db.session.commit()
    return jsonify({'mensaje': 'Estado de casilla actualizado'})

@casillas_estados_bp.route('/<int:casilla_estado_id>', methods=['DELETE'])
def eliminar_casilla_estado(casilla_estado_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
    casilla_estado = CasillaEstado.query.get(casilla_estado_id)
    if not casilla_estado:
        return jsonify({'mensaje': 'Estado de casilla no encontrado'}), 404
    db.session.delete(casilla_estado)
    db.session.commit()
    return jsonify({'mensaje': 'Estado de casilla eliminado'})