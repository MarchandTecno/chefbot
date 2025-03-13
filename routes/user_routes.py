# routes/user_routes.py
from flask import Blueprint, request, jsonify
from handlers.user_handler import get_or_create_user, get_user, update_user, delete_user

user_bp = Blueprint('user', __name__)

@user_bp.route("/start", methods=["POST"])
def start():
    data = request.get_json()
    try:
        # Se busca o crea el usuario en la base de datos
        user = get_or_create_user(data)
        return jsonify({"message": f"¡Hola, {user['name']}! ¿Te gustaría ver el menú?"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user_route(user_id):
    try:
        user = get_user(user_id)
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    data = request.get_json()
    try:
        user = update_user(user_id, data)
        return jsonify({"message": "Usuario actualizado correctamente", "user": user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    try:
        delete_user(user_id)
        return jsonify({"message": "Usuario eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
