from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import (
    Partida,
    Tablero,
    Casilla,
    PersonajePartida,
    Personaje,
    JugadorPersonaje,
)
from logica.casillas import aplicar_efectos_casilla
from logica.tablero import generar_tablero
from logica.dados import lanzar_dados
from app import socketio

partidas_bp = Blueprint("partidas", __name__)

INV_CSRF = 'CSRF token inválido'


@partidas_bp.route('/', methods=['POST'])
def crear_partida():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': INV_CSRF}), 400
    data = request.get_json()
    nombre = data.get('nombre')
    tamano_tablero = data.get('tamano_tablero')
    dificultad = data.get('dificultad')

    if not nombre or not tamano_tablero or not dificultad:
        return jsonify({'mensaje': 'Nombre, tamaño del tablero y dificultad son requeridos'}), 400

    nueva_partida = Partida(nombre=nombre, tamano_tablero=tamano_tablero, dificultad=dificultad)
    db.session.add(nueva_partida)
    db.session.flush()  # necesario para obtener el id de la partida

    # generar tablero
    generar_tablero(nueva_partida, tamano_tablero, dificultad)

    db.session.commit()
    return jsonify({'mensaje': 'Partida creada', 'id': nueva_partida.id}), 201


@partidas_bp.route("/<int:partida_id>", methods=["GET"])
@csrf.exempt
def obtener_partida(partida_id):
    partida = Partida.query.get(partida_id)
    if not partida:
        return jsonify({"mensaje": "Partida no encontrada"}), 404
    return jsonify(
        {"id": partida.id, "tableroId": partida.tableroId, "estado": partida.estado}
    )


@partidas_bp.route("/<int:partida_id>/unirse", methods=["POST"])
def unirse_partida(partida_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': INV_CSRF}), 400
    data = request.get_json()
    personaje_id = data.get("personajeId")
    jugador_id = data.get("jugadorId")  # agregado jugadorId
    partida = Partida.query.get(partida_id)
    personaje = Personaje.query.get(personaje_id)

    if not partida or not personaje:
        return jsonify({"mensaje": "Partida o personaje no encontrado"}), 404

    # Nueva verificación usando JugadorPersonaje
    jugador_personaje = JugadorPersonaje.query.filter_by(
        jugadorId=jugador_id, personajeId=personaje_id
    ).first()
    if not jugador_personaje:
        return jsonify(
            {"mensaje": "El personaje no está asignado a este jugador"}
        ), 400

    socketio.emit(
        "jugador_unido",
        {"partida_id": partida_id, "personaje_id": personaje_id, "jugador_id": jugador_id},
        room=partida_id,
    )  # Enviar mensaje de WebSocket
    return jsonify({"mensaje": "Personaje unido a la partida"}), 200

@partidas_bp.route("/<int:partida_id>/<int:personaje_id>/estado", methods=["GET"])
@csrf.exempt
def obtener_estado_personaje_partida(partida_id, personaje_id):
    personaje_partida = PersonajePartida.query.filter_by(
        partidaId=partida_id, personajeId=personaje_id
    ).first()
    if not personaje_partida:
        return jsonify({"mensaje": "Estado de personaje en partida no encontrado"}), 404
    return jsonify(
        {
            "partidaId": personaje_partida.partidaId,
            "personajeId": personaje_partida.personajeId,
            "posicion": personaje_partida.posicion,
            "vida": personaje_partida.vida,
            "oro": personaje_partida.oro,
        }
    )

@partidas_bp.route("/<int:partida_id>/mover", methods=["POST"])
def mover_personaje(partida_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': INV_CSRF}), 400
    data = request.get_json()
    personaje_id = data.get("personajeId")
    jugador_id = data.get("jugadorId")  # agregado jugadorId
    partida = Partida.query.get(partida_id)
    personaje = Personaje.query.get(personaje_id)

    if not partida or not personaje:
        return jsonify({"mensaje": "Partida o personaje no encontrado"}), 404

    # Nueva verificación usando JugadorPersonaje
    jugador_personaje = JugadorPersonaje.query.filter_by(
        jugadorId=jugador_id, personajeId=personaje_id
    ).first()
    if not jugador_personaje:
        return jsonify(
            {"mensaje": "El personaje no está asignado a este jugador"}
        ), 400

    dado1, dado2, movimiento = lanzar_dados()  # agregar los dados lanzados.

    tablero = Tablero.query.get(partida.tableroId)
    casillas = eval(tablero.casillas)

    posicion_actual = obtener_posicion_personaje(personaje, partida_id)
    nueva_posicion = posicion_actual + movimiento

    if nueva_posicion >= len(casillas):
        return jsonify({"mensaje": "No puedes moverte más allá del tablero"}), 400

    nueva_casilla = Casilla.query.get(casillas[nueva_posicion]["id"])

    aplicar_efectos_casilla(personaje, nueva_casilla, partida_id)

    # Actualiza PersonajePartida
    personaje_partida = PersonajePartida.query.filter_by(
        partidaId=partida_id, personajeId=personaje.id
    ).first()
    personaje_partida.posicion = nueva_posicion
    db.session.commit()

    socketio.emit(
        "personaje_movido",
        {
            "partida_id": partida_id,
            "personaje_id": personaje_id,
            "nueva_posicion": nueva_posicion,
            "dados": (dado1, dado2),  # agregar los dados lanzados.
        },
        room=partida_id,
    )  # Enviar mensaje de WebSocket

    return (
        jsonify({"mensaje": "Personaje movido", "nuevaPosicion": nueva_posicion}),
        200,
    )


def obtener_posicion_personaje(personaje, partida_id):
    personaje_partida = PersonajePartida.query.filter_by(
        partidaId=partida_id, personajeId=personaje.id
    ).first()
    return personaje_partida.posicion


def obtener_tipos_casillas():
    tipos_casillas = [
        casilla.tipo for casilla in Casilla.query.distinct(Casilla.tipo).all()
    ]
    return tipos_casillas