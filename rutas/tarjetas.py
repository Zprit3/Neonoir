from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import Tarjeta

tarjetas_bp = Blueprint('tarjetas', __name__)

TARJETA_NF = 'Tarjeta no encontrada'
CSRF_INV = 'CSRF token inválido'

@tarjetas_bp.route('/', methods=['GET'])
@csrf.exempt
def obtener_tarjetas():
    tarjetas = Tarjeta.query.all()
    lista_tarjetas = [{'id': tarjeta.id, 'nombre': tarjeta.nombre, 'descripcion': tarjeta.descripcion, 'tipo': tarjeta.tipo, 'efecto': tarjeta.efecto, 'duracion': tarjeta.duracion} for tarjeta in tarjetas]
    return jsonify(lista_tarjetas)

@tarjetas_bp.route('/<int:tarjeta_id>', methods=['GET'])
@csrf.exempt
def obtener_tarjeta(tarjeta_id):
    tarjeta = Tarjeta.query.get(tarjeta_id)
    if not tarjeta:
        return jsonify({'mensaje': TARJETA_NF}), 404
    return jsonify({'id': tarjeta.id, 'nombre': tarjeta.nombre, 'descripcion': tarjeta.descripcion, 'tipo': tarjeta.tipo, 'efecto': tarjeta.efecto, 'duracion': tarjeta.duracion})

@tarjetas_bp.route('/', methods=['POST'])
def crear_tarjeta():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    data = request.get_json()
    nombre = data.get('nombre')
    tipo = data.get('tipo')
    if not nombre or not tipo:
        return jsonify({'mensaje': 'Nombre y tipo son requeridos'}), 400
    nueva_tarjeta = Tarjeta(nombre=nombre, tipo=tipo)
    db.session.add(nueva_tarjeta)
    db.session.commit()
    return jsonify({'mensaje': 'Tarjeta creada', 'id': nueva_tarjeta.id}), 201

@tarjetas_bp.route('/<int:tarjeta_id>', methods=['PUT'])
def actualizar_tarjeta(tarjeta_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    tarjeta = Tarjeta.query.get(tarjeta_id)
    if not tarjeta:
        return jsonify({'mensaje': TARJETA_NF}), 404
    data = request.get_json()
    tarjeta.nombre = data.get('nombre', tarjeta.nombre)
    tarjeta.descripcion = data.get('descripcion', tarjeta.descripcion)
    tarjeta.tipo = data.get('tipo', tarjeta.tipo)
    tarjeta.efecto = data.get('efecto', tarjeta.efecto)
    tarjeta.duracion = data.get('duracion', tarjeta.duracion)
    db.session.commit()
    return jsonify({'mensaje': 'Tarjeta actualizada'})

@tarjetas_bp.route('/<int:tarjeta_id>', methods=['DELETE'])
def eliminar_tarjeta(tarjeta_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    tarjeta = Tarjeta.query.get(tarjeta_id)
    if not tarjeta:
        return jsonify({'mensaje': CSRF_INV}), 404
    db.session.delete(tarjeta)
    db.session.commit()
    return jsonify({'mensaje': 'Tarjeta eliminada'})