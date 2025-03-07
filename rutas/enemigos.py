from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import Enemigo, PersonajePartida, Tarjeta, PersonajeTarjetas
import random
from app import socketio

ENEMIGO_NF = 'Enemigo no encontrado'
CSRF_INV = 'CSRF token inválido'

enemigos_bp = Blueprint('enemigos', __name__)

@enemigos_bp.route('/', methods=['GET'])
@csrf.exempt
def obtener_enemigos():
    enemigos = Enemigo.query.all()
    lista_enemigos = [{'id': enemigo.id, 'nombre': enemigo.nombre, 'vida': enemigo.vida, 'tipo': enemigo.tipo, 'oroDrop': enemigo.oroDrop, 'tarjetaDropId': enemigo.tarjetaDropId} for enemigo in enemigos]
    return jsonify(lista_enemigos)

@enemigos_bp.route('/<int:enemigo_id>', methods=['GET'])
@csrf.exempt
def obtener_enemigo(enemigo_id):
    enemigo = Enemigo.query.get(enemigo_id)
    if not enemigo:
        return jsonify({'mensaje': ENEMIGO_NF}), 404
    return jsonify({'id': enemigo.id, 'nombre': enemigo.nombre, 'vida': enemigo.vida, 'tipo': enemigo.tipo, 'oroDrop': enemigo.oroDrop, 'tarjetaDropId': enemigo.tarjetaDropId})

@enemigos_bp.route('/', methods=['POST'])
def crear_enemigo():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    data = request.get_json()
    nombre = data.get('nombre')
    vida = data.get('vida')
    tipo = data.get('tipo')
    if not nombre or not vida or not tipo:
        return jsonify({'mensaje': 'Nombre, vida y tipo son requeridos'}), 400
    nuevo_enemigo = Enemigo(nombre=nombre, vida=vida, tipo=tipo)
    db.session.add(nuevo_enemigo)
    db.session.commit()
    return jsonify({'mensaje': 'Enemigo creado', 'id': nuevo_enemigo.id}), 201

@enemigos_bp.route('/<int:enemigo_id>', methods=['PUT'])
def actualizar_enemigo(enemigo_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    enemigo = Enemigo.query.get(enemigo_id)
    if not enemigo:
        return jsonify({'mensaje': ENEMIGO_NF}), 404
    data = request.get_json()
    enemigo.nombre = data.get('nombre', enemigo.nombre)
    enemigo.vida = data.get('vida', enemigo.vida)
    enemigo.tipo = data.get('tipo', enemigo.tipo)
    enemigo.oroDrop = data.get('oroDrop', enemigo.oroDrop)
    enemigo.tarjetaDropId = data.get('tarjetaDropId', enemigo.tarjetaDropId)
    db.session.commit()
    return jsonify({'mensaje': 'Enemigo actualizado'})

@enemigos_bp.route('/<int:enemigo_id>', methods=['DELETE'])
def eliminar_enemigo(enemigo_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    enemigo = Enemigo.query.get(enemigo_id)
    if not enemigo:
        return jsonify({'mensaje': ENEMIGO_NF}), 404
    db.session.delete(enemigo)
    db.session.commit()
    return jsonify({'mensaje': 'Enemigo eliminado'})

@enemigos_bp.route('/<int:enemigo_id>/derrotar/<int:personaje_partida_id>', methods=['POST'])
def derrotar_enemigo(enemigo_id, personaje_partida_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    enemigo = Enemigo.query.get(enemigo_id)
    personaje_partida = PersonajePartida.query.get(personaje_partida_id)

    if not enemigo or not personaje_partida:
        return jsonify({'mensaje': 'Enemigo o estado de personaje no encontrado'}), 404

    # Lógica para el loot (ejemplo)
    oro_obtenido = 0
    tarjeta_obtenida = None

    if enemigo.oroDrop > 0:
        personaje_partida.oro += enemigo.oroDrop
        oro_obtenido = enemigo.oroDrop
    if enemigo.tarjetaDropId:
        tarjeta = Tarjeta.query.get(enemigo.tarjetaDropId)
        if tarjeta.unica:
            personaje_tarjeta = PersonajeTarjetas.query.filter_by(personajeId=personaje_partida.personajeId, tarjetaId=tarjeta.id).first()
            if not personaje_tarjeta:
                nuevo_personaje_tarjeta = PersonajeTarjetas(personajeId=personaje_partida.personajeId, tarjetaId=tarjeta.id)
                db.session.add(nuevo_personaje_tarjeta)
                tarjeta_obtenida = tarjeta.id
        else:
            personaje_tarjeta = PersonajeTarjetas.query.filter_by(personajeId=personaje_partida.personajeId, tarjetaId=tarjeta.id).first()
            if personaje_tarjeta:
                personaje_tarjeta.cantidad += 1
            else:
                nuevo_personaje_tarjeta = PersonajeTarjetas(personajeId=personaje_partida.personajeId, tarjetaId=tarjeta.id)
                db.session.add(nuevo_personaje_tarjeta)
            tarjeta_obtenida = tarjeta.id

    db.session.delete(enemigo)
    db.session.commit()

    socketio.emit('enemigo_derrotado', {'personaje_partida_id': personaje_partida_id, 'oro_obtenido': oro_obtenido, 'tarjeta_obtenida': tarjeta_obtenida}, room=personaje_partida.partidaId) #emitir derrota de enemigo.

    return jsonify({'mensaje': 'Enemigo derrotado y loot obtenido'})