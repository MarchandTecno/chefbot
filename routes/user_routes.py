from flask import Blueprint, request, jsonify
from handlers.user_handler import get_or_create_user, get_user, update_user, delete_user

user_bp = Blueprint('user', __name__)

@user_bp.route("/start", methods=["POST"])
def start():
    """
    Iniciar sesión o crear usuario.
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: Juan Pérez
    responses:
      200:
        description: Usuario creado o encontrado.
      500:
        description: Error interno.
    """
    data = request.get_json()
    try:
        user = get_or_create_user(data)
        return jsonify({"message": f"¡Hola, {user['name']}! ¿Te gustaría ver el menú?"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user_route(user_id):
    """
    Obtener información de un usuario.
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID del usuario a buscar.
    responses:
      200:
        description: Información del usuario.
      404:
        description: Usuario no encontrado.
    """
    try:
        user = get_user(user_id)
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    """
    Actualizar información de un usuario.
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID del usuario a actualizar.
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
              example: Juan Pérez
            email:
              type: string
              example: juan@example.com
    responses:
      200:
        description: Usuario actualizado correctamente.
      500:
        description: Error interno.
    """
    data = request.get_json()
    try:
        user = update_user(user_id, data)
        return jsonify({"message": "Usuario actualizado correctamente", "user": user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    """
    Eliminar un usuario.
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID del usuario a eliminar.
    responses:
      200:
        description: Usuario eliminado correctamente.
      500:
        description: Error interno.
    """
    try:
        delete_user(user_id)
        return jsonify({"message": "Usuario eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
