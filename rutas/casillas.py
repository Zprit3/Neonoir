from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import Casilla

casillas_bp = Blueprint('casillas', __name__)

CASILLA_NF = 'Casilla no encontrada'
CSRF_INV = 'CSRF token inválido'

@casillas_bp.route('/', methods=['GET'])
@csrf.exempt
def obtener_casillas():
    casillas = Casilla.query.all()
    lista_casillas = [{'id': casilla.id, 'tipo': casilla.tipo} for casilla in casillas]
    return jsonify(lista_casillas)

@casillas_bp.route('/<int:casilla_id>', methods=['GET'])
@csrf.exempt
def obtener_casilla(casilla_id):
    casilla = Casilla.query.get(casilla_id)
    if not casilla:
        return jsonify({'mensaje': CASILLA_NF}), 404
    return jsonify({'id': casilla.id, 'tipo': casilla.tipo})

@casillas_bp.route('/', methods=['POST'])
def crear_casilla():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    data = request.get_json()
    tipo = data.get('tipo')
    if not tipo:
        return jsonify({'mensaje': 'Tipo es requerido'}), 400
    nueva_casilla = Casilla(tipo=tipo)
    db.session.add(nueva_casilla)
    db.session.commit()
    return jsonify({'mensaje': 'Casilla creada', 'id': nueva_casilla.id}), 201

@casillas_bp.route('/<int:casilla_id>', methods=['PUT'])
def actualizar_casilla(casilla_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    casilla = Casilla.query.get(casilla_id)
    if not casilla:
        return jsonify({'mensaje': CASILLA_NF}), 404
    data = request.get_json()
    casilla.tipo = data.get('tipo', casilla.tipo)
    db.session.commit()
    return jsonify({'mensaje': 'Casilla actualizada'})

@casillas_bp.route('/<int:casilla_id>', methods=['DELETE'])
def eliminar_casilla(casilla_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    casilla = Casilla.query.get(casilla_id)
    if not casilla:
        return jsonify({'mensaje': CASILLA_NF}), 404
    db.session.delete(casilla)
    db.session.commit()
    return jsonify({'mensaje': 'Casilla eliminada'})