from flask import Blueprint, request, jsonify
from extensions import db
from models import Jugador

jugadores_bp = Blueprint('jugadores', __name__)

@jugadores_bp.route('/', methods=['GET'])
def obtener_jugadores():
    jugadores = Jugador.query.all()
    lista_jugadores = [{'id': jugador.id, 'nombre_usuario': jugador.nombreUsuario, 'puntaje': jugador.puntaje} for jugador in jugadores]
    return jsonify(lista_jugadores)

@jugadores_bp.route('/<int:jugador_id>', methods=['GET'])
def obtener_jugador(jugador_id):
    jugador = Jugador.query.get(jugador_id)
    if not jugador:
        return jsonify({'mensaje': 'Jugador no encontrado'}), 404
    return jsonify({'id': jugador.id, 'nombre_usuario': jugador.nombreUsuario, 'puntaje': jugador.puntaje})

@jugadores_bp.route('/', methods=['POST'])
def crear_jugador():
    data = request.get_json()
    nombre_usuario = data.get('nombreUsuario')
    contrasena = data.get('contrasena')
    if not nombre_usuario or not contrasena:
        return jsonify({'mensaje': 'Nombre de usuario y contraseña son requeridos'}), 400
    nuevo_jugador = Jugador(nombreUsuario=nombre_usuario, contrasena=contrasena)
    db.session.add(nuevo_jugador)
    db.session.commit()
    return jsonify({'mensaje': 'Jugador creado', 'id': nuevo_jugador.id}), 201

@jugadores_bp.route('/<int:jugador_id>', methods=['PUT'])
def actualizar_jugador(jugador_id):
    jugador = Jugador.query.get(jugador_id)
    if not jugador:
        return jsonify({'mensaje': 'Jugador no encontrado'}), 404
    data = request.get_json()
    jugador.nombreUsuario = data.get('nombreUsuario', jugador.nombreUsuario)
    jugador.contrasena = data.get('contrasena', jugador.contrasena)
    jugador.puntaje = data.get('puntaje', jugador.puntaje)
    db.session.commit()
    return jsonify({'mensaje': 'Jugador actualizado'})

@jugadores_bp.route('/<int:jugador_id>', methods=['DELETE'])
def eliminar_jugador(jugador_id):
    jugador = Jugador.query.get(jugador_id)
    if not jugador:
        return jsonify({'mensaje': 'Jugador no encontrado'}), 404
    db.session.delete(jugador)
    db.session.commit()
    return jsonify({'mensaje': 'Jugador eliminado'})