from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import Jugador, Personaje, JugadorPersonaje

jugadores_bp = Blueprint('jugadores', __name__)

JUGADOR_NF = 'Jugador no encontrado'
CSRF_INV = 'CSRF token inválido'

@jugadores_bp.route('/', methods=['GET'])
@csrf.exempt
def obtener_jugadores():
    jugadores = Jugador.query.all()
    lista_jugadores = []
    for jugador in jugadores:
        personajes_asociados = []
        jugador_personajes = JugadorPersonaje.query.filter_by(jugadorId=jugador.id).all()
        for jp in jugador_personajes:
            personaje = Personaje.query.get(jp.personajeId)
            if personaje:
                personajes_asociados.append({
                    'id': personaje.id,
                    'nombre': personaje.nombre,
                    'vida': personaje.vida,
                    'estadisticaPrincipal': personaje.estadisticaPrincipal,
                    'oro': personaje.oro
                })
        lista_jugadores.append({
            'id': jugador.id,
            'nombreUsuario': jugador.nombreUsuario,
            'puntaje': jugador.puntaje,
            'personajes': personajes_asociados
        })
    return jsonify(lista_jugadores)

@jugadores_bp.route('/<int:jugador_id>', methods=['GET'])
@csrf.exempt
def obtener_jugador(jugador_id):
    jugador = Jugador.query.get(jugador_id)
    if not jugador:
        return jsonify({'mensaje': JUGADOR_NF}), 404
    personajes_asociados = []
    jugador_personajes = JugadorPersonaje.query.filter_by(jugadorId=jugador.id).all()
    for jp in jugador_personajes:
        personaje = Personaje.query.get(jp.personajeId)
        if personaje:
            personajes_asociados.append({
                'id': personaje.id,
                'nombre': personaje.nombre,
                'vida': personaje.vida,
                'estadisticaPrincipal': personaje.estadisticaPrincipal,
                'oro': personaje.oro
            })
    return jsonify({
        'id': jugador.id,
        'nombreUsuario': jugador.nombreUsuario,
        'puntaje': jugador.puntaje,
        'personajes': personajes_asociados
    })

@jugadores_bp.route('/', methods=['POST'])
def crear_jugador():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
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
        return jsonify({'mensaje': CSRF_INV}), 400
    jugador = Jugador.query.get(jugador_id)
    if not jugador:
        return jsonify({'mensaje': JUGADOR_NF}), 404
    data = request.get_json()
    jugador.nombreUsuario = data.get('nombreUsuario', jugador.nombreUsuario)
    if data.get('contrasena'):
        jugador.set_password(data.get('contrasena'))
    jugador.puntaje = data.get('puntaje', jugador.puntaje)
    db.session.commit()
    return jsonify({'mensaje': 'Jugador actualizado'})

@jugadores_bp.route('/<int:jugador_id>', methods=['DELETE'])
def eliminar_jugador(jugador_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    jugador = Jugador.query.get(jugador_id)
    if not jugador:
        return jsonify({'mensaje': JUGADOR_NF}), 404
    db.session.delete(jugador)
    db.session.commit()
    return jsonify({'mensaje': 'Jugador eliminado'})