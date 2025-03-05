from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import Zona

zonas_bp = Blueprint('zonas', __name__)

@zonas_bp.route('/', methods=['GET'])
@csrf.exempt
def obtener_zonas():
    zonas = Zona.query.all()
    lista_zonas = [{'id': zona.id, 'tipoZona': zona.tipoZona, 'recuperacionVida': zona.recuperacionVida, 'limpiarDebuffs': zona.limpiarDebuffs, 'probabilidadObjetoVictoria': zona.probabilidadObjetoVictoria, 'modificacionVida': zona.modificacionVida, 'debuffEstadistica': zona.debuffEstadistica, 'retornoZonaDescanso': zona.retornoZonaDescanso, 'descripcion': zona.descripcion} for zona in zonas]
    return jsonify(lista_zonas)

@zonas_bp.route('/<int:zona_id>', methods=['GET'])
@csrf.exempt
def obtener_zona(zona_id):
    zona = Zona.query.get(zona_id)
    if not zona:
        return jsonify({'mensaje': 'Zona no encontrada'}), 404
    return jsonify({'id': zona.id, 'tipoZona': zona.tipoZona, 'recuperacionVida': zona.recuperacionVida, 'limpiarDebuffs': zona.limpiarDebuffs, 'probabilidadObjetoVictoria': zona.probabilidadObjetoVictoria, 'modificacionVida': zona.modificacionVida, 'debuffEstadistica': zona.debuffEstadistica, 'retornoZonaDescanso': zona.retornoZonaDescanso, 'descripcion': zona.descripcion})

@zonas_bp.route('/', methods=['POST'])
def crear_zona():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
    data = request.get_json()
    tipo_zona = data.get('tipoZona')
    if not tipo_zona:
        return jsonify({'mensaje': 'Tipo de zona es requerido'}), 400
    nueva_zona = Zona(tipoZona=tipo_zona)
    db.session.add(nueva_zona)
    db.session.commit()
    return jsonify({'mensaje': 'Zona creada', 'id': nueva_zona.id}), 201

@zonas_bp.route('/<int:zona_id>', methods=['PUT'])
def actualizar_zona(zona_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
    zona = Zona.query.get(zona_id)
    if not zona:
        return jsonify({'mensaje': 'Zona no encontrada'}), 404
    data = request.get_json()
    zona.tipoZona = data.get('tipoZona', zona.tipoZona)
    zona.recuperacionVida = data.get('recuperacionVida', zona.recuperacionVida)
    zona.limpiarDebuffs = data.get('limpiarDebuffs', zona.limpiarDebuffs)
    zona.probabilidadObjetoVictoria = data.get('probabilidadObjetoVictoria', zona.probabilidadObjetoVictoria)
    zona.modificacionVida = data.get('modificacionVida', zona.modificacionVida)
    zona.debuffEstadistica = data.get('debuffEstadistica', zona.debuffEstadistica)
    zona.retornoZonaDescanso = data.get('retornoZonaDescanso', zona.retornoZonaDescanso)
    zona.descripcion = data.get('descripcion', zona.descripcion)
    db.session.commit()
    return jsonify({'mensaje': 'Zona actualizada'})

@zonas_bp.route('/<int:zona_id>', methods=['DELETE'])
def eliminar_zona(zona_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': 'CSRF token inválido'}), 400
    zona = Zona.query.get(zona_id)
    if not zona:
        return jsonify({'mensaje': 'Zona no encontrada'}), 404
    db.session.delete(zona)
    db.session.commit()
    return jsonify({'mensaje': 'Zona eliminada'})