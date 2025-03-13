# handlers/start_handler.py
from flask import jsonify, request
from handlers.user_handler import get_or_create_user

def start():
    data = request.get_json()
    if not data or "user_id" not in data or "name" not in data:
        return jsonify({"error": "Faltan datos del usuario"}), 400
    try:
        # get_or_create_user() debe buscar el usuario por ID y, si no existe, crearlo
        user = get_or_create_user(data)
        return jsonify({"message": f"¡Hola {user['name']}! Soy tu asistente de pedidos. ¿Te gustaría ver el menú?"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
