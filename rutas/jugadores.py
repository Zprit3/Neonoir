from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import Jugador

jugadores_bp = Blueprint('jugadores', __name__)

@jugadores_bp.route('/', methods=['GET'])
@csrf.exempt # Eximir la protección CSRF para esta ruta
def obtener_jugadores():
    jugadores = Jugador.query.all()
    lista_jugadores = [{'id': jugador.id, 'nombre_usuario': jugador.nombreUsuario, 'puntaje': jugador.puntaje} for jugador in jugadores]
    return jsonify(lista_jugadores)

@jugadores_bp.route('/<int:jugador_id>', methods=['GET'])
@csrf.exempt # Eximir la protección CSRF para esta ruta
def obtener_jugador(jugador_id):
    jugador = Jugador.query.get(jugador_id)
    if not jugador:
        return jsonify({'mensaje': 'Jugador no encontrado'}), 404
    return jsonify({'id': jugador.id, 'nombre_usuario': jugador.nombreUsuario, 'puntaje': jugador.puntaje})

@jugadores_bp.route('/', methods=['POST'])
def crear_jugador():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
    data = request.get_json()
    nombre_usuario = data.get('nombreUsuario')
    contrasena = data.get('contrasena')
    if not nombre_usuario or not contrasena:
        return jsonify({'mensaje': 'Nombre de usuario y contraseña son requeridos'}), 400
    nuevo_jugador = Jugador(nombreUsuario=nombre_usuario)
    nuevo_jugador.set_password(contrasena)
    db.session.add(nuevo_jugador)
    db.session.commit()
    return jsonify({'mensaje': 'Jugador creado', 'id': nuevo_jugador.id}), 201

@jugadores_bp.route('/<int:jugador_id>', methods=['PUT'])
def actualizar_jugador(jugador_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
    jugador = Jugador.query.get(jugador_id)
    if not jugador:
        return jsonify({'mensaje': 'Jugador no encontrado'}), 404
    data = request.get_json()
    jugador.nombreUsuario = data.get('nombreUsuario', jugador.nombreUsuario)
    nueva_contrasena = data.get('contrasena')
    if nueva_contrasena:
        jugador.set_password(nueva_contrasena)
    jugador.puntaje = data.get('puntaje', jugador.puntaje)
    db.session.commit()
    return jsonify({'mensaje': 'Jugador actualizado'})

@jugadores_bp.route('/<int:jugador_id>', methods=['DELETE'])
def eliminar_jugador(jugador_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
    jugador = Jugador.query.get(jugador_id)
    if not jugador:
        return jsonify({'mensaje': 'Jugador no encontrado'}), 404
    db.session.delete(jugador)
    db.session.commit()
    return jsonify({'mensaje': 'Jugador eliminado'})