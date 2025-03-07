from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import ObjetoVictoria

objetos_victoria_bp = Blueprint('objetos_victoria', __name__)

CSRF_INV = 'CSRF token inválido'
OB_VIC_NF = 'Objeto de victoria no encontrado'

@objetos_victoria_bp.route('/', methods=['GET'])
@csrf.exempt
def obtener_objetos_victoria():
    objetos_victoria = ObjetoVictoria.query.all()
    lista_objetos_victoria = [{'id': objeto_victoria.id, 'nombre': objeto_victoria.nombre, 'descripcion': objeto_victoria.descripcion} for objeto_victoria in objetos_victoria]
    return jsonify(lista_objetos_victoria)

@objetos_victoria_bp.route('/<int:objeto_victoria_id>', methods=['GET'])
@csrf.exempt
def obtener_objeto_victoria(objeto_victoria_id):
    objeto_victoria = ObjetoVictoria.query.get(objeto_victoria_id)
    if not objeto_victoria:
        return jsonify({'mensaje': OB_VIC_NF}), 404
    return jsonify({'id': objeto_victoria.id, 'nombre': objeto_victoria.nombre, 'descripcion': objeto_victoria.descripcion})

@objetos_victoria_bp.route('/', methods=['POST'])
def crear_objeto_victoria():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    if not nombre or not descripcion:
        return jsonify({'mensaje': 'Nombre y descripción son requeridos'}), 400
    nuevo_objeto_victoria = ObjetoVictoria(nombre=nombre, descripcion=descripcion)
    db.session.add(nuevo_objeto_victoria)
    db.session.commit()
    return jsonify({'mensaje': 'Objeto de victoria creado', 'id': nuevo_objeto_victoria.id}), 201

@objetos_victoria_bp.route('/<int:objeto_victoria_id>', methods=['PUT'])
def actualizar_objeto_victoria(objeto_victoria_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    objeto_victoria = ObjetoVictoria.query.get(objeto_victoria_id)
    if not objeto_victoria:
        return jsonify({'mensaje': OB_VIC_NF}), 404
    data = request.get_json()
    objeto_victoria.nombre = data.get('nombre', objeto_victoria.nombre)
    objeto_victoria.descripcion = data.get('descripcion', objeto_victoria.descripcion)
    db.session.commit()
    return jsonify({'mensaje': 'Objeto de victoria actualizado'})

@objetos_victoria_bp.route('/<int:objeto_victoria_id>', methods=['DELETE'])
def eliminar_objeto_victoria(objeto_victoria_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    objeto_victoria = ObjetoVictoria.query.get(objeto_victoria_id)
    if not objeto_victoria:
        return jsonify({'mensaje': OB_VIC_NF}), 404
    db.session.delete(objeto_victoria)
    db.session.commit()
    return jsonify({'mensaje': 'Objeto de victoria eliminado'})