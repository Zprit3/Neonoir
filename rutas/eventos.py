from flask import Blueprint, request, jsonify
from extensions import db
from models import Evento

eventos_bp = Blueprint('eventos', __name__)

@eventos_bp.route('/', methods=['GET'])
def obtener_eventos():
    eventos = Evento.query.all()
    lista_eventos = [{'id': evento.id, 'nombre': evento.nombre, 'descripcion': evento.descripcion, 'avanceCasillas': evento.avanceCasillas, 'modificacionOro': evento.modificacionOro, 'modificacionVida': evento.modificacionVida, 'debuffEstadistica': evento.debuffEstadistica, 'duracionDebuffCasillas': evento.duracionDebuffCasillas, 'npcId': evento.npcId} for evento in eventos]
    return jsonify(lista_eventos)

@eventos_bp.route('/<int:evento_id>', methods=['GET'])
def obtener_evento(evento_id):
    evento = Evento.query.get(evento_id)
    if not evento:
        return jsonify({'mensaje': 'Evento no encontrado'}), 404
    return jsonify({'id': evento.id, 'nombre': evento.nombre, 'descripcion': evento.descripcion, 'avanceCasillas': evento.avanceCasillas, 'modificacionOro': evento.modificacionOro, 'modificacionVida': evento.modificacionVida, 'debuffEstadistica': evento.debuffEstadistica, 'duracionDebuffCasillas': evento.duracionDebuffCasillas, 'npcId': evento.npcId})

@eventos_bp.route('/', methods=['POST'])
def crear_evento():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    if not nombre or not descripcion:
        return jsonify({'mensaje': 'Nombre y descripción son requeridos'}), 400
    nuevo_evento = Evento(nombre=nombre, descripcion=descripcion)
    db.session.add(nuevo_evento)
    db.session.commit()
    return jsonify({'mensaje': 'Evento creado', 'id': nuevo_evento.id}), 201

@eventos_bp.route('/<int:evento_id>', methods=['PUT'])
def actualizar_evento(evento_id):
    evento = Evento.query.get(evento_id)
    if not evento:
        return jsonify({'mensaje': 'Evento no encontrado'}), 404
    data = request.get_json()
    evento.nombre = data.get('nombre', evento.nombre)
    evento.descripcion = data.get('descripcion', evento.descripcion)
    evento.avanceCasillas = data.get('avanceCasillas', evento.avanceCasillas)
    evento.modificacionOro = data.get('modificacionOro', evento.modificacionOro)
    evento.modificacionVida = data.get('modificacionVida', evento.modificacionVida)
    evento.debuffEstadistica = data.get('debuffEstadistica', evento.debuffEstadistica)
    evento.duracionDebuffCasillas = data.get('duracionDebuffCasillas', evento.duracionDebuffCasillas)
    evento.npcId = data.get('npcId', evento.npcId)
    db.session.commit()
    return jsonify({'mensaje': 'Evento actualizado'})

@eventos_bp.route('/<int:evento_id>', methods=['DELETE'])
def eliminar_evento(evento_id):
    evento = Evento.query.get(evento_id)
    if not evento:
        return jsonify({'mensaje': 'Evento no encontrado'}), 404
    db.session.delete(evento)
    db.session.commit()
    return jsonify({'mensaje': 'Evento eliminado'})