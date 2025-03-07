from flask import Blueprint, jsonify, make_response
from flask_wtf.csrf import generate_csrf

csrf_bp = Blueprint('csrf', __name__)

@csrf_bp.route('/csrf-token', methods=['GET'])
def get_csrf_token():
    csrf_token = generate_csrf()
    response = make_response(jsonify({'csrf_token': csrf_token}))
    return response