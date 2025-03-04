from flask import Blueprint, request, jsonify
from extensions import db
from models import Partida, Tablero, Casilla, PersonajePartida, Personaje
from logica.casillas import aplicar_efectos_casilla 
import random

partidas_bp = Blueprint('partidas', __name__)

def lanzar_dados():
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    return dado1 + dado2

@partidas_bp.route('/', methods=['POST'])
def crear_partida():
    tablero = generar_tablero()
    nuevo_tablero = Tablero(casillas=str(tablero))
    db.session.add(nuevo_tablero)
    db.session.commit()

    nueva_partida = Partida(tableroId=nuevo_tablero.id)
    db.session.add(nueva_partida)
    db.session.commit()

    # Crea PersonajePartida para cada casilla
    for casilla in tablero:
        personaje_partida = PersonajePartida(partidaId=nueva_partida.id, casillaId=casilla['id'])
        db.session.add(personaje_partida)
    db.session.commit()

    return jsonify({'mensaje': 'Partida creada', 'id': nueva_partida.id}), 201

@partidas_bp.route('/<int:partida_id>', methods=['GET'])
def obtener_partida(partida_id):
    partida = Partida.query.get(partida_id)
    if not partida:
        return jsonify({'mensaje': 'Partida no encontrada'}), 404
    return jsonify({'id': partida.id, 'tableroId': partida.tableroId, 'estado': partida.estado})

@partidas_bp.route('/<int:partida_id>/unirse', methods=['POST'])
def unirse_partida(partida_id):
    data = request.get_json()
    personaje_id = data.get('personajeId')
    partida = Partida.query.get(partida_id)
    personaje = Personaje.query.get(personaje_id)

    if not partida or not personaje:
        return jsonify({'mensaje': 'Partida o personaje no encontrado'}), 404

    if personaje.jugadorId != partida_id:
        return jsonify({'mensaje': 'El personaje no está en esta partida'}), 400

    return jsonify({'mensaje': 'Personaje unido a la partida'}), 200

@partidas_bp.route('/<int:partida_id>/mover', methods=['POST'])
def mover_personaje(partida_id):
    data = request.get_json()
    personaje_id = data.get('personajeId')
    partida = Partida.query.get(partida_id)
    personaje = Personaje.query.get(personaje_id)

    if not partida or not personaje:
        return jsonify({'mensaje': 'Partida o personaje no encontrado'}), 404

    if personaje.jugadorId != partida_id:
        return jsonify({'mensaje': 'El personaje no está en esta partida'}), 400

    movimiento = lanzar_dados()

    tablero = Tablero.query.get(partida.tableroId)
    casillas = eval(tablero.casillas)

    posicion_actual = obtener_posicion_personaje(personaje, partida_id)
    nueva_posicion = posicion_actual + movimiento

    if nueva_posicion >= len(casillas):
        return jsonify({'mensaje': 'No puedes moverte más allá del tablero'}), 400

    nueva_casilla = Casilla.query.get(casillas[nueva_posicion]['id'])

    aplicar_efectos_casilla(personaje, nueva_casilla, partida_id)

    # Actualiza PersonajePartida
    personaje_partida = PersonajePartida.query.filter_by(partidaId=partida_id, personajeId=personaje.id).first()
    personaje_partida.posicion = nueva_posicion
    db.session.commit()

    return jsonify({'mensaje': 'Personaje movido', 'nuevaPosicion': nueva_posicion}), 200

def obtener_posicion_personaje(personaje, partida_id):
    personaje_partida = PersonajePartida.query.filter_by(partidaId=partida_id, personajeId=personaje.id).first()
    return personaje_partida.posicion

def generar_tablero():
    cantidad_casillas = random.randint(100, 200)
    casillas = []
    tipos_casillas = obtener_tipos_casillas()
    for _ in range(cantidad_casillas):
        tipo = random.choice(tipos_casillas)
        casilla = Casilla(tipo=tipo)
        db.session.add(casilla)
        db.session.commit()
        casillas.append({'id': casilla.id, 'tipo': tipo})
    return casillas

def obtener_tipos_casillas():
    tipos_casillas = [casilla.tipo for casilla in Casilla.query.distinct(Casilla.tipo).all()]
    return tipos_casillas