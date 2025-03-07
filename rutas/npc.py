from flask import Blueprint, request, jsonify
from extensions import db, csrf
from models import Npc

npc_bp = Blueprint('npcs', __name__)

NPC_NF = 'NPC no encontrado'
CSRF_INV = 'CSRF token inválido'

@npc_bp.route('/', methods=['GET'])
@csrf.exempt
def obtener_npcs():
    npcs = Npc.query.all()
    lista_npcs = [{'id': npc.id, 'nombre': npc.nombre, 'dialogo': npc.dialogo} for npc in npcs]
    return jsonify(lista_npcs)

@npc_bp.route('/<int:npc_id>', methods=['GET'])
@csrf.exempt
def obtener_npc(npc_id):
    npc = Npc.query.get(npc_id)
    if not npc:
        return jsonify({'mensaje': NPC_NF}), 404
    return jsonify({'id': npc.id, 'nombre': npc.nombre, 'dialogo': npc.dialogo})

@npc_bp.route('/', methods=['POST'])
def crear_npc():
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    data = request.get_json()
    nombre = data.get('nombre')
    dialogo = data.get('dialogo')
    if not nombre or not dialogo:
        return jsonify({'mensaje': 'Nombre y diálogo son requeridos'}), 400
    nuevo_npc = Npc(nombre=nombre, dialogo=dialogo)
    db.session.add(nuevo_npc)
    db.session.commit()
    return jsonify({'mensaje': 'NPC creado', 'id': nuevo_npc.id}), 201

@npc_bp.route('/<int:npc_id>', methods=['PUT'])
def actualizar_npc(npc_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    npc = Npc.query.get(npc_id)
    if not npc:
        return jsonify({'mensaje': NPC_NF}), 404
    data = request.get_json()
    npc.nombre = data.get('nombre', npc.nombre)
    npc.dialogo = data.get('dialogo', npc.dialogo)
    db.session.commit()
    return jsonify({'mensaje': 'NPC actualizado'})

@npc_bp.route('/<int:npc_id>', methods=['DELETE'])
def eliminar_npc(npc_id):
    if not csrf.validate_csrf(request.headers.get('X-CSRFToken')):
        return jsonify({'mensaje': CSRF_INV}), 400
    npc = Npc.query.get(npc_id)
    if not npc:
        return jsonify({'mensaje': NPC_NF}), 404
    db.session.delete(npc)
    db.session.commit()
    return jsonify({'mensaje': 'NPC eliminado'})