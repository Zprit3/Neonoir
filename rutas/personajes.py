from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import Personaje, JugadorPersonaje
from app import socketio

personajes_bp = Blueprint('personajes', __name__)

MENSAJE = 'Personaje no encontrado'
INV_CSRF = 'CSRF token inválido'

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
        return jsonify({'mensaje': MENSAJE}), 404
    return jsonify({'id': personaje.id, 'nombre': personaje.nombre, 'vida': personaje.vida, 'estadisticaPrincipal': personaje.estadisticaPrincipal, 'oro': personaje.oro})

@personajes_bp.route('/', methods=['POST'])
def crear_personaje():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': INV_CSRF}), 400
    data = request.get_json()
    nombre = data.get('nombre')
    vida = data.get('vida')
    estadistica_principal = data.get('estadisticaPrincipal')
    if not nombre or not vida or not estadistica_principal:
        return jsonify({'mensaje': 'Nombre, vida y estadisticaPrincipal son requeridos'}), 400
    nuevo_personaje = Personaje(nombre=nombre, vida=vida, estadisticaPrincipal=estadistica_principal)
    db.session.add(nuevo_personaje)
    db.session.commit()
    return jsonify({'mensaje': 'Personaje creado', 'id': nuevo_personaje.id}), 201

@personajes_bp.route('/<int:personaje_id>', methods=['PUT'])
def actualizar_personaje(personaje_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': INV_CSRF}), 400
    personaje = Personaje.query.get(personaje_id)
    if not personaje:
        return jsonify({'mensaje': MENSAJE}), 404
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
        return jsonify({'mensaje': INV_CSRF}), 400
    personaje = Personaje.query.get(personaje_id)
    if not personaje:
        return jsonify({'mensaje': MENSAJE}), 404
    db.session.delete(personaje)
    db.session.commit()
    return jsonify({'mensaje': 'Personaje eliminado'})

# Rutas para JugadorPersonaje
@personajes_bp.route('/<int:personaje_id>/asignar/<int:jugador_id>', methods=['POST'])
def asignar_personaje_a_jugador(personaje_id, jugador_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': INV_CSRF}), 400
    jugador_personaje = JugadorPersonaje(jugadorId=jugador_id, personajeId=personaje_id)
    db.session.add(jugador_personaje)
    db.session.commit()
    socketio.emit('personaje_asignado', {'personaje_id': personaje_id, 'jugador_id': jugador_id}, room=jugador_id)
    return jsonify({'mensaje': 'Personaje asignado al jugador'})

@personajes_bp.route('/<int:personaje_id>/desasignar/<int:jugador_id>', methods=['DELETE'])
def desasignar_personaje_de_jugador(personaje_id, jugador_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': INV_CSRF}), 400
    jugador_personaje = JugadorPersonaje.query.filter_by(jugadorId=jugador_id, personajeId=personaje_id).first()
    if not jugador_personaje:
        return jsonify({'mensaje': 'Asignación no encontrada'}), 404
    db.session.delete(jugador_personaje)
    db.session.commit()
    socketio.emit('personaje_desasignado', {'personaje_id': personaje_id, 'jugador_id': jugador_id}, room=jugador_id)
    return jsonify({'mensaje': 'Personaje desasignado del jugador'})