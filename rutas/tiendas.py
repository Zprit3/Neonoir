from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import Tienda, Tarjeta, PersonajePartida, PersonajeTarjetas
from app import socketio

tiendas_bp = Blueprint('tiendas', __name__)

TIENDA_NF = 'Tienda no encontrada'
CSRF_INV = 'CSRF token inválido'

@tiendas_bp.route('/', methods=['GET'])
@csrf.exempt
def obtener_tiendas():
    tiendas = Tienda.query.all()
    lista_tiendas = [{'id': tienda.id, 'nombre': tienda.nombre, 'tarjetas_venta': tienda.tarjetas_venta} for tienda in tiendas]
    return jsonify(lista_tiendas)

@tiendas_bp.route('/<int:tienda_id>', methods=['GET'])
@csrf.exempt
def obtener_tienda(tienda_id):
    tienda = Tienda.query.get(tienda_id)
    if not tienda:
        return jsonify({'mensaje': TIENDA_NF}), 404
    return jsonify({'id': tienda.id, 'nombre': tienda.nombre, 'tarjetas_venta': tienda.tarjetas_venta})

@tiendas_bp.route('/', methods=['POST'])
def crear_tienda():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    data = request.get_json()
    nombre = data.get('nombre')
    tarjetas_venta = data.get('tarjetas_venta')
    if not nombre:
        return jsonify({'mensaje': 'Nombre es requerido'}), 400
    nueva_tienda = Tienda(nombre=nombre, tarjetas_venta=tarjetas_venta)
    db.session.add(nueva_tienda)
    db.session.commit()
    return jsonify({'mensaje': 'Tienda creada', 'id': nueva_tienda.id}), 201

@tiendas_bp.route('/<int:tienda_id>', methods=['PUT'])
def actualizar_tienda(tienda_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    tienda = Tienda.query.get(tienda_id)
    if not tienda:
        return jsonify({'mensaje': TIENDA_NF}), 404
    data = request.get_json()
    tienda.nombre = data.get('nombre', tienda.nombre)
    tienda.tarjetas_venta = data.get('tarjetas_venta', tienda.tarjetas_venta)
    db.session.commit()
    return jsonify({'mensaje': 'Tienda actualizada'})

@tiendas_bp.route('/<int:tienda_id>', methods=['DELETE'])
def eliminar_tienda(tienda_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    tienda = Tienda.query.get(tienda_id)
    if not tienda:
        return jsonify({'mensaje': TIENDA_NF}), 404
    db.session.delete(tienda)
    db.session.commit()
    return jsonify({'mensaje': 'Tienda eliminada'})

@tiendas_bp.route('/<int:tienda_id>/tarjetas', methods=['GET'])
@csrf.exempt
def obtener_tarjetas_tienda(tienda_id):
    tienda = Tienda.query.get(tienda_id)
    if not tienda:
        return jsonify({'mensaje': TIENDA_NF}), 404
    return jsonify(tienda.tarjetas_venta)

@tiendas_bp.route('/<int:tienda_id>/comprar/<int:personaje_partida_id>/<int:tarjeta_id>', methods=['POST'])
def comprar_tarjeta(tienda_id, personaje_partida_id, tarjeta_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    tienda = Tienda.query.get(tienda_id)
    personaje_partida = PersonajePartida.query.get(personaje_partida_id)
    tarjeta = Tarjeta.query.get(tarjeta_id)

    if not tienda or not personaje_partida or not tarjeta:
        return jsonify({'mensaje': 'Tienda, personaje o tarjeta no encontrada'}), 404

    # Verificar si la tarjeta está en venta y si el personaje tiene suficiente oro
    tarjeta_venta = next((t for t in tienda.tarjetas_venta if t['tarjeta_id'] == tarjeta_id), None)
    if not tarjeta_venta or personaje_partida.oro < tarjeta_venta['precio']:
        return jsonify({'mensaje': 'Tarjeta no disponible o oro insuficiente'}), 400

    # Agregar la tarjeta al inventario del personaje
    personaje_tarjeta = PersonajeTarjetas.query.filter_by(personajeId=personaje_partida.personajeId, tarjetaId=tarjeta.id).first()
    if personaje_tarjeta:
        personaje_tarjeta.cantidad += 1
    else:
        nuevo_personaje_tarjeta = PersonajeTarjetas(personajeId=personaje_partida.personajeId, tarjetaId=tarjeta.id)
        db.session.add(nuevo_personaje_tarjeta)

    # Restar el oro del personaje
    personaje_partida.oro -= tarjeta_venta['precio']

    db.session.commit()

    socketio.emit('tarjeta_comprada', {'personaje_partida_id': personaje_partida_id, 'tarjeta_id': tarjeta_id}, room=personaje_partida.partidaId) #emitir compra de tarjeta.
    return jsonify({'mensaje': 'Tarjeta comprada'})