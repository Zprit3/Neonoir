from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import Personaje

personajes_bp = Blueprint('personajes', __name__)

@personajes_bp.route('/', methods=['GET'])
@csrf.exempt
def obtener_personajes():
    personajes = Personaje.query.all()
    lista_personajes = [{'id': personaje.id, 'nombre': personaje.nombre, 'vida': personaje.vida, 'estadisticaPrincipal': personaje.estadisticaPrincipal, 'oro': personaje.oro} for personaje in personajes]
    return jsonify(lista_personajes)

@personajes_bp.route('/<int:personaje_id>', methods=['GET'])
@csrf.exempt
def obtener_personaje(personaje_id):
    personaje = Personaje.query.get(personaje_id)
    if not personaje:
        return jsonify({'mensaje': 'Personaje no encontrado'}), 404
    return jsonify({'id': personaje.id, 'nombre': personaje.nombre, 'vida': personaje.vida, 'estadisticaPrincipal': personaje.estadisticaPrincipal, 'oro': personaje.oro})

@personajes_bp.route('/', methods=['POST'])
def crear_personaje():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
    data = request.get_json()
    jugador_id = data.get('jugadorId')
    nombre = data.get('nombre')
    if not jugador_id or not nombre:
        return jsonify({'mensaje': 'jugadorId y nombre son requeridos'}), 400
    nuevo_personaje = Personaje(jugadorId=jugador_id, nombre=nombre)
    db.session.add(nuevo_personaje)
    db.session.commit()
    return jsonify({'mensaje': 'Personaje creado', 'id': nuevo_personaje.id}), 201

@personajes_bp.route('/<int:personaje_id>', methods=['PUT'])
def actualizar_personaje(personaje_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
    personaje = Personaje.query.get(personaje_id)
    if not personaje:
        return jsonify({'mensaje': 'Personaje no encontrado'}), 404
    data = request.get_json()
    personaje.nombre = data.get('nombre', personaje.nombre)
    personaje.vida = data.get('vida', personaje.vida)
    personaje.estadisticaPrincipal = data.get('estadisticaPrincipal', personaje.estadisticaPrincipal)
    personaje.oro = data.get('oro', personaje.oro)
    db.session.commit()
    return jsonify({'mensaje': 'Personaje actualizado'})

@personajes_bp.route('/<int:personaje_id>', methods=['DELETE'])
def eliminar_personaje(personaje_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
    personaje = Personaje.query.get(personaje_id)
    if not personaje:
        return jsonify({'mensaje': 'Personaje no encontrado'}), 404
    db.session.delete(personaje)
    db.session.commit()
    return jsonify({'mensaje': 'Personaje eliminado'})