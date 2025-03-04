from flask import Blueprint, request, jsonify
from extensions import db
from models import Npc

npcs_bp = Blueprint('npcs', __name__)

@npcs_bp.route('/', methods=['GET'])
def obtener_npcs():
    npcs = Npc.query.all()
    lista_npcs = [{'id': npc.id, 'nombre': npc.nombre, 'dialogo': npc.dialogo} for npc in npcs]
    return jsonify(lista_npcs)

@npcs_bp.route('/<int:npc_id>', methods=['GET'])
def obtener_npc(npc_id):
    npc = Npc.query.get(npc_id)
    if not npc:
        return jsonify({'mensaje': 'NPC no encontrado'}), 404
    return jsonify({'id': npc.id, 'nombre': npc.nombre, 'dialogo': npc.dialogo})

@npcs_bp.route('/', methods=['POST'])
def crear_npc():
    data = request.get_json()
    nombre = data.get('nombre')
    dialogo = data.get('dialogo')
    if not nombre or not dialogo:
        return jsonify({'mensaje': 'Nombre y diálogo son requeridos'}), 400
    nuevo_npc = Npc(nombre=nombre, dialogo=dialogo)
    db.session.add(nuevo_npc)
    db.session.commit()
    return jsonify({'mensaje': 'NPC creado', 'id': nuevo_npc.id}), 201

@npcs_bp.route('/<int:npc_id>', methods=['PUT'])
def actualizar_npc(npc_id):
    npc = Npc.query.get(npc_id)
    if not npc:
        return jsonify({'mensaje': 'NPC no encontrado'}), 404
    data = request.get_json()
    npc.nombre = data.get('nombre', npc.nombre)
    npc.dialogo = data.get('dialogo', npc.dialogo)
    db.session.commit()
    return jsonify({'mensaje': 'NPC actualizado'})

@npcs_bp.route('/<int:npc_id>', methods=['DELETE'])
def eliminar_npc(npc_id):
    npc = Npc.query.get(npc_id)
    if not npc:
        return jsonify({'mensaje': 'NPC no encontrado'}), 404
    db.session.delete(npc)
    db.session.commit()
    return jsonify({'mensaje': 'NPC eliminado'})